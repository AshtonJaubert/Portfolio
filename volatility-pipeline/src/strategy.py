import yfinance as yf
import pandas as pd
import numpy as np
import QuantLib as ql
import quantstats as qs
from loguru import logger
import sys
import os

# --- BOILERPLATE ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# --- CONFIGURATION ---
PORTFOLIO = config.PORTFOLIO
INDICES = ['SPY', 'QQQ', 'IWM', 'SPYI', 'DIA']

# --- STRATEGY PARAMETERS ---
INITIAL_CAPITAL = 100000
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.75
TARGET_PORTFOLIO_VOL = 0.20
TAKE_PROFIT_PCT = 0.80
STOP_LOSS_PCT = -0.85

# --- LOGGING SETUP ---
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# --- QUANTLIB PRICING ---
def ql_black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    Prices an option using QuantLib.
    """
    try:
        # Calendar and DayCount
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        day_count = ql.Actual365Fixed()
        
        # Date Setup
        today_ql = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today_ql
        maturity_date = today_ql + int(T * 365)

        # Market Data Handles
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(S))
        rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today_ql, r, day_count))
        vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today_ql, calendar, sigma, day_count))
        
        # Process
        bsm_process = ql.BlackScholesProcess(spot_handle, rate_handle, vol_handle)
        
        # Option Object
        option_type_ql = ql.Option.Call if option_type == 'call' else ql.Option.Put
        payoff = ql.PlainVanillaPayoff(option_type_ql, K)
        exercise = ql.EuropeanExercise(maturity_date)
        option = ql.VanillaOption(payoff, exercise)
        
        # Engine
        option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
        
        return option.NPV()
    except Exception as e:
        logger.error(f"QuantLib Pricing Error: {e}")
        return 0.0

def get_condor_price(S, strikes, T, r, sigma):
    p_sp = ql_black_scholes_price(S, strikes['sp'], T, r, sigma, 'put')
    p_lp = ql_black_scholes_price(S, strikes['lp'], T, r, sigma, 'put')
    p_sc = ql_black_scholes_price(S, strikes['sc'], T, r, sigma, 'call')
    p_lc = ql_black_scholes_price(S, strikes['lc'], T, r, sigma, 'call')
    return (p_sp + p_sc) - (p_lp + p_lc)

def run_ticker_backtest(ticker):
    is_index = ticker in getattr(config, 'INDICES', INDICES)
    logger.info(f"Backtesting {ticker}...")
    
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        df = df[[col]].rename(columns={col: 'price'})
    except Exception as e:
        logger.error(f"Failed to download {ticker}: {e}")
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
    
    i = 50
    while i < len(days) - 5:
        curr_date = days[i]
        vol_rank = df.loc[curr_date]['vol_rank']
        
        trade_approved = False
        if vol_rank > VOL_PERCENTILE_THRESHOLD:
            # Simple check for now
            trade_approved = True
        
        if trade_approved:
            trade_count += 1
            entry_price = df.loc[curr_date]['price']
            iv = df.loc[curr_date]['iv_proxy']
            current_vol = df.loc[curr_date]['rolling_vol']
            
            strikes = {
                'sp': entry_price * 0.96, 'lp': entry_price * 0.90,
                'sc': entry_price * 1.04, 'lc': entry_price * 1.10
            }
            
            T_entry = 7 / 365.0
            entry_credit = max(0.01, get_condor_price(entry_price, strikes, T_entry, r, iv))
            
            vol_scaler = max(0.1, min(TARGET_PORTFOLIO_VOL / current_vol, 2.0))
            max_risk = (strikes['sp'] - strikes['lp']) 
            qty = int((capital * 0.05 * vol_scaler) / (max_risk * 100))
            qty = max(1, qty)
            
            total_max_profit = entry_credit * 100 * qty
            
            trade_closed = False
            pnl = 0
            days_held = 5
            
            for d in range(1, 6):
                sim_date = days[i + d]
                sim_price = df.loc[sim_date]['price']
                sim_iv = df.loc[sim_date]['iv_proxy']
                T_curr = (7 - d) / 365.0
                
                curr_value = get_condor_price(sim_price, strikes, T_curr, r, sim_iv)
                pnl_pct = (entry_credit - curr_value) / entry_credit
                
                if pnl_pct >= TAKE_PROFIT_PCT:
                    pnl = total_max_profit * TAKE_PROFIT_PCT
                    trade_closed = True
                    wins += 1
                    days_held = d
                    break
                
                if pnl_pct <= STOP_LOSS_PCT:
                    pnl = total_max_profit * STOP_LOSS_PCT
                    trade_closed = True
                    losses += 1
                    days_held = d
                    break
            
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

    # Convert to Series for QuantStats
    equity_series = pd.Series(equity_curve, index=dates)
    returns_series = equity_series.pct_change().fillna(0)
    
    # Generate QuantStats Report (Optional: saves HTML)
    # qs.reports.html(returns_series, output=f"{ticker}_quantstats.html", title=f"{ticker} Analysis")
    
    total_ret = ((capital - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
    sharpe = qs.stats.sharpe(returns_series)
    max_dd = qs.stats.max_drawdown(returns_series)
    
    logger.success(f"{ticker} Result: ${capital:,.0f} | Ret: {total_ret:.1f}% | Sharpe: {sharpe:.2f} | Max DD: {max_dd:.1%}")
    
    return {
        "Ticker": ticker,
        "Total Profit": capital - INITIAL_CAPITAL,
        "Trades": trade_count,
        "Wins": wins,
        "Losses": losses,
        "Max DD": max_dd
    }

def run_backtest():
    logger.info("Starting QuantStats Backtest Cycle")
    results = []
    for ticker in PORTFOLIO:
        res = run_ticker_backtest(ticker)
        if res: results.append(res)

    if results:
        df = pd.DataFrame(results)
        logger.info(f"🏆 TOTAL PROFIT:   ${df['Total Profit'].sum():,.2f}")

if __name__ == "__main__":
    run_backtest()
