import yfinance as yf
import pandas as pd
import numpy as np
import sys
import os
from scipy.stats import norm

# --- BOILERPLATE ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# --- CONFIGURATION ---
PORTFOLIO = config.PORTFOLIO
INDICES = ['SPY', 'QQQ', 'IWM', 'SPYI', 'DIA']

# --- STRATEGY PARAMETERS ---
INITIAL_CAPITAL = 100000
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.75  # Entry: Vol > 75%
TARGET_PORTFOLIO_VOL = 0.20

# --- EXIT RULES ---
TAKE_PROFIT_PCT = 0.80  # Close at 80% Profit (Aggressive take profit)
STOP_LOSS_PCT = -0.85   # Stop at 85% Loss

# --- PRICING MODELS ---
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    try:
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    except:
        return 0.0

def get_condor_price(S, strikes, T, r, sigma):
    """Calculates the current market price to close the Iron Condor."""
    p_sp = black_scholes_price(S, strikes['sp'], T, r, sigma, 'put')
    p_lp = black_scholes_price(S, strikes['lp'], T, r, sigma, 'put')
    p_sc = black_scholes_price(S, strikes['sc'], T, r, sigma, 'call')
    p_lc = black_scholes_price(S, strikes['lc'], T, r, sigma, 'call')
    return (p_sp + p_sc) - (p_lp + p_lc)

def calculate_max_drawdown(equity_curve):
    equity_curve = np.array(equity_curve)
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max
    return drawdown.min()

def run_ticker_backtest(ticker):
    print(f"\nBacktesting {ticker} (2020 Bear Market Test)...")
    
    try:
        # Downloading from Nov 2022 to ensure indicators are ready by Jan 1, 2023
        df = yf.download(ticker, start="2023-11-01", end="2024-12-31", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        df = df[[col]].rename(columns={col: 'price'})
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        return None

    # Metrics
    df['returns'] = df['price'].pct_change()
    df['rolling_vol'] = df['returns'].rolling(VOL_LOOKBACK).std() * np.sqrt(252)
    df['vol_rank'] = df['rolling_vol'].rank(pct=True)
    df['iv_proxy'] = df['rolling_vol'] * 1.2
    
    capital = INITIAL_CAPITAL
    equity_curve = [INITIAL_CAPITAL]
    dates = [df.index[0]]
    
    trade_count = 0
    wins = 0
    losses = 0
    days = list(df.index)
    r = 0.04
    
    # Loop through days
    i = 50
    while i < len(days) - 5:
        curr_date = days[i]
        vol_rank = df.loc[curr_date]['vol_rank']
        
        # --- ENTRY CHECK ---
        # 1. First, check if the trade meets the volatility threshold
        if vol_rank > VOL_PERCENTILE_THRESHOLD:
            trade_approved = True
        else:
            trade_approved = False

        if trade_approved:
            trade_count += 1
            
            # 2. DEFINE VARIABLES (Must happen first)
            entry_price = df.loc[curr_date]['price']
            iv = df.loc[curr_date]['iv_proxy']
            current_vol = df.loc[curr_date]['rolling_vol']
            
            # 3. DEFINE STRIKES
            strikes = {
                'sp': entry_price * 0.96, 'lp': entry_price * 0.90,
                'sc': entry_price * 1.04, 'lc': entry_price * 1.10
            }
            
            # 4. CALCULATE PRICING
            T_entry = 7 / 365.0
            entry_credit = max(0.01, get_condor_price(entry_price, strikes, T_entry, r, iv))
            
            # 5. SIZING LOGIC
            vol_scaler = max(0.1, min(TARGET_PORTFOLIO_VOL / current_vol, 2.0))
            
            # --- AGGRESSIVE LOGIC ---
            # Double size if volatility is extreme (>95th percentile)
            aggressive_multiplier = 1.0
            if vol_rank > 0.95:
                aggressive_multiplier = 2.0
                
            max_risk_per_share = (strikes['sp'] - strikes['lp']) 
            qty = int((capital * 0.05 * vol_scaler * aggressive_multiplier) / (max_risk_per_share * 100))
            qty = max(1, qty)
            
            total_max_profit = entry_credit * 100 * qty
            
            # 6. MANAGE TRADE (Day 1 to 5)
            trade_closed = False
            pnl = 0
            days_held = 5
            
            for d in range(1, 6):
                sim_date = days[i + d]
                sim_price = df.loc[sim_date]['price']
                sim_iv = df.loc[sim_date]['iv_proxy']
                T_curr = (7 - d) / 365.0
                
                # Mark to Market
                curr_value = get_condor_price(sim_price, strikes, T_curr, r, sim_iv)
                
                # PnL %
                pnl_pct = (entry_credit - curr_value) / entry_credit
                
                # CHECK PROFIT TARGET
                if pnl_pct >= TAKE_PROFIT_PCT:
                    pnl = total_max_profit * TAKE_PROFIT_PCT
                    trade_closed = True
                    wins += 1
                    days_held = d
                    break
                
                # CHECK STOP LOSS
                if pnl_pct <= STOP_LOSS_PCT:
                    pnl = total_max_profit * STOP_LOSS_PCT
                    trade_closed = True
                    losses += 1
                    days_held = d
                    break
            
            # 7. EXPIRATION
            if not trade_closed:
                end_price = df.loc[days[i+5]]['price']
                loss_put = max(0, strikes['sp'] - end_price) - max(0, strikes['lp'] - end_price)
                loss_call = max(0, end_price - strikes['sc']) - max(0, end_price - strikes['lc'])
                expiry_loss = (loss_put + loss_call) * 100 * qty
                
                pnl = total_max_profit - expiry_loss
                if pnl > 0: wins += 1
                else: losses += 1
            
            capital += pnl
            equity_curve.append(capital)
            i += days_held 
            dates.append(days[i])
            
        else:
            i += 1
            equity_curve.append(capital)
            dates.append(days[i])

    # Reporting
    total_ret = ((capital - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
    daily_rets = pd.Series(equity_curve).pct_change().fillna(0)
    sharpe = 0 if daily_rets.std() == 0 else daily_rets.mean() / daily_rets.std() * np.sqrt(252)
    max_dd = calculate_max_drawdown(equity_curve)
    
    print(f"   Final: ${capital:,.0f} | Ret: {total_ret:.1f}% | Sharpe: {sharpe:.2f} | Max DD: {max_dd:.1%}")
    
    return {
        "Ticker": ticker,
        "Total Profit": capital - INITIAL_CAPITAL,
        "Trades": trade_count,
        "Wins": wins,
        "Losses": losses,
        "Max DD": max_dd
    }

def run_backtest():
    print("\n=======================================================")
    print(f"   ACTIVE MANAGEMENT BACKTEST (2022)")
    print(f"   Exit Winners @ {TAKE_PROFIT_PCT:.0%} | Stop Losers @ {STOP_LOSS_PCT:.0%}")
    print("=======================================================\n")
    
    results = []
    for ticker in PORTFOLIO:
        res = run_ticker_backtest(ticker)
        if res: results.append(res)

    if results:
        df = pd.DataFrame(results)
        print("\n-------------------------------------------------------")
        print(f"   🏆 TOTAL PROFIT:   ${df['Total Profit'].sum():,.2f}")
        print(f"   🎯 WIN RATE:       {(df['Wins'].sum()/df['Trades'].sum()*100):.1f}%")
        print("-------------------------------------------------------")

if __name__ == "__main__":
    run_backtest()