import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# --- BOILERPLATE: Allow importing config from root folder ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# --- CONFIGURATION ---
TICKER = config.TARGET_TICKER
INITIAL_CAPITAL = 10000

# --- "REALITY GAP" PARAMETERS ---
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.80  # Trade when Vol is in Top 20%

# Trade Structure: IRON CONDOR (Defined Risk)
# We sell the 4% OTM strikes, and BUY the 10% OTM strikes for protection.
SHORT_STRIKE_PCT = 0.04   # 4% Out of the Money (Sell Strike)
WING_WIDTH_PCT = 0.06     # Wings are 6% wide (Buy Strike is 10% OTM)
PREMIUM_COLLECTED = 300   # Reduced from $500 to account for buying wings + slippage

def calculate_max_drawdown(equity_curve):
    equity_curve = np.array(equity_curve)
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max
    return drawdown.min()

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    if np.std(returns) == 0:
        return 0
    excess_returns = returns - (risk_free_rate / 252)
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def run_backtest():
    print(f"--- Starting Defined Risk (Iron Condor) Backtest for {TICKER} ---\n")
    
    # 1. Fetch Historical Data
    print("Fetching 1 year of daily price data...")
    df = yf.download(TICKER, period="1y", interval="1d")
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    col_name = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
    df = df[[col_name]].copy()
    df.rename(columns={col_name: 'price'}, inplace=True)

    # 2. Calculate Volatility Regime
    df['returns'] = df['price'].pct_change()
    df['rolling_vol'] = df['returns'].rolling(window=VOL_LOOKBACK).std() * np.sqrt(252)
    df['vol_rank'] = df['rolling_vol'].rank(pct=True)

    # 3. Strategy Logic Loop
    capital = INITIAL_CAPITAL
    equity_curve = [INITIAL_CAPITAL]
    dates = [df.index[0]]
    trade_count = 0
    skipped_trades = 0
    daily_returns = []

    days = list(df.index)
    
    print(f"Scanning for High Volatility opportunities (Top {(1-VOL_PERCENTILE_THRESHOLD)*100:.0f}%)...")
    
    for i in range(VOL_LOOKBACK, len(days) - 5, 5): 
        current_date = days[i]
        future_date_idx = i + 5
        
        if future_date_idx < len(days):
            current_vol_rank = df.loc[current_date]['vol_rank']
            
            # SIGNAL: Only trade if Vol Rank > 80% (Panic)
            if current_vol_rank > VOL_PERCENTILE_THRESHOLD:
                trade_count += 1
                today_price = df.loc[current_date]['price']
                future_price = df.loc[days[future_date_idx]]['price']
                
                pct_move = abs(future_price - today_price) / today_price
                
                # --- DEFINED RISK LOGIC ---
                if pct_move > SHORT_STRIKE_PCT:
                    # 1. Calculate Raw Loss (how much past the short strike are we?)
                    raw_loss_per_share = (pct_move - SHORT_STRIKE_PCT) * today_price
                    
                    # 2. Cap the Loss (The "Iron Condor" Wing Protection)
                    # We cannot lose more than the width of the wings
                    max_loss_per_share = WING_WIDTH_PCT * today_price
                    
                    # Realized loss is the smaller of the two
                    realized_loss_per_share = min(raw_loss_per_share, max_loss_per_share)
                    
                    loss_amt = realized_loss_per_share * 100
                    pnl = PREMIUM_COLLECTED - loss_amt
                else:
                    # Stock stayed within range
                    pnl = PREMIUM_COLLECTED
                    
                prev_capital = capital
                capital += pnl
                daily_returns.append((capital - prev_capital) / prev_capital)
                
            else:
                skipped_trades += 1
                daily_returns.append(0)
                
            equity_curve.append(capital)
            dates.append(days[future_date_idx])

    # 4. Metrics & Reporting
    total_return_pct = ((capital - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
    max_dd = calculate_max_drawdown(equity_curve)
    sharpe = calculate_sharpe_ratio(np.array(daily_returns))

    print("\n" + "="*40)
    print(f"      REALITY CHECK RESULTS: {TICKER}")
    print("      (Iron Condor Model)")
    print("="*40)
    print(f"Trades Taken:      {trade_count}")
    print(f"Trades Skipped:    {skipped_trades}")
    print(f"Final Capital:     ${capital:,.2f}")
    print(f"Total Return:      {total_return_pct:.2f}%")
    print(f"Max Drawdown:      {max_dd*100:.2f}%")
    print(f"Sharpe Ratio:      {sharpe:.2f}")
    print("="*40 + "\n")
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, equity_curve, label='Defined Risk Strategy', color='purple', linewidth=2)
    plt.axhline(y=INITIAL_CAPITAL, color='gray', linestyle='--', label='Initial Capital')
    plt.title(f'Defined Risk (Iron Condor): {TICKER}\nCapped Losses | Sharpe: {sharpe:.2f}')
    plt.xlabel('Date')
    plt.ylabel('Account Value ($)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    output_filename = f"{TICKER}_RealityCheck_Report.png"
    plt.savefig(output_filename)
    print(f"✅ Equity curve saved to: {output_filename}")
    plt.show()

if __name__ == "__main__":
    run_backtest()