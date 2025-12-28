import pandas as pd
import sys
import os
import yfinance as yf
import numpy as np


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config 

# --- STRATEGY SETTINGS ---
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.75  # Entry Threshold
AGGRESSIVE_THRESHOLD = 0.95      # Double Size Threshold

def analyze_data():
    print("=====================================================")
    print(f"   INSTITUTIONAL ANALYTICS: {len(config.PORTFOLIO)} ASSETS")
    print(f"   Logic: Entry > {VOL_PERCENTILE_THRESHOLD:.0%} | Aggressive > {AGGRESSIVE_THRESHOLD:.0%}")
    print("=====================================================\n")
    
    for ticker in config.PORTFOLIO:
        try:
            # Fetch Data
            # We need 1 year to calculate an accurate percentile rank
            df = yf.download(ticker, period="1y", interval="1d", progress=False)
            
            # Handle MultiIndex headers (common yfinance issue)
            if isinstance(df.columns, pd.MultiIndex): 
                df.columns = df.columns.get_level_values(0)
            
            col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
            if df.empty: 
                print(f"   ❌ {ticker}: No data found.")
                continue

            # 2. Calculate Volatility Metrics
            df['returns'] = df[col].pct_change()
            df['rolling_vol'] = df['returns'].rolling(VOL_LOOKBACK).std() * np.sqrt(252)
            
            current_vol = df['rolling_vol'].iloc[-1]
            current_price = df[col].iloc[-1]
            
            # Rank: How often was volatility LOWER than it is today?
            vol_rank = (df['rolling_vol'] < current_vol).mean()
            
            # 3. Determine Status
            status_icon = "💤"
            status_msg = "WAIT (Vol too low)"
            
            if vol_rank > AGGRESSIVE_THRESHOLD:
                status_icon = "🔥"
                status_msg = "AGGRESSIVE (Double Size)"
            elif vol_rank > VOL_PERCENTILE_THRESHOLD:
                status_icon = "✅"
                status_msg = "TRADE (Standard Size)"
            
            # 4. Print Report
            print(f"{status_icon} {ticker:<6} | Price: ${current_price:<8.2f} | Vol Rank: {vol_rank:.1%} | {status_msg}")

        except Exception as e:
            print(f"   ❌ {ticker}: Error ({e})")

    print("\n=====================================================")
    print("   ANALYSIS COMPLETE")
    print("=====================================================")

if __name__ == "__main__":
    analyze_data()