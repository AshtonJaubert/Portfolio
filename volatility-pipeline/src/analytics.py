import pandas as pd
from sqlalchemy import create_engine, inspect
import sys
import os
import yfinance as yf
import numpy as np

# Allow importing from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def analyze_data():
    print(f"--- Analytics for {config.TARGET_TICKER} ---")
    
    # 1. LIVE VOLATILITY REGIME (The "Hunting" Logic)
    # We fetch history here to see where TODAY stands relative to the past year
    print("\n[1] Calculating Volatility Rank...")
    try:
        # Fetch 1 year of history
        hist = yf.download(config.TARGET_TICKER, period="1y", interval="1d", progress=False)
        
        # Handle MultiIndex if present
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
            
        col_name = 'Adj Close' if 'Adj Close' in hist.columns else 'Close'
        hist['returns'] = hist[col_name].pct_change()
        
        # Calculate 20-day Realized Volatility
        hist['rolling_vol'] = hist['returns'].rolling(window=20).std() * np.sqrt(252)
        
        # Calculate Rank
        current_vol = hist['rolling_vol'].iloc[-1]
        # Percentile rank of current vol against the last year
        vol_rank = (hist['rolling_vol'] < current_vol).mean()
        
        print(f"    Current Realized Vol: {current_vol*100:.2f}%")
        print(f"    Yearly Vol Rank:      {vol_rank*100:.0f}% (Percentile)")
        
        # Signal Check
        if vol_rank > 0.80:
            print("    👉 SIGNAL: TRADE ACTIVE (Volatility is Expensive)")
        else:
            print("    👉 SIGNAL: STAND ASIDE (Volatility is Cheap)")
            
    except Exception as e:
        print(f"    ⚠️ Could not calculate Vol Rank: {e}")

    # 2. OPTION FLOW (Database Check)
    print("\n[2] Checking Option Sentiment (Database)...")
    connection_str = f"sqlite:///{config.DB_NAME}"
    engine = create_engine(connection_str)
    
    target_table = "options_history"
    inspector = inspect(engine)
    
    if target_table not in inspector.get_table_names():
        print(f"    ❌ Table '{target_table}' NOT found. Run data_ingestion.py first.")
        return

    # Fetch Data
    query = f"SELECT * FROM {target_table} WHERE ticker = '{config.TARGET_TICKER}'"
    df = pd.read_sql(query, engine)

    if df.empty:
        print(f"    ❌ No option data found for {config.TARGET_TICKER}.")
        return

    # Put/Call Ratio Calculation
    if 'Type' in df.columns:
        call_count = len(df[df['Type'] == 'Call'])
        put_count = len(df[df['Type'] == 'Put'])
        ratio = put_count / call_count if call_count > 0 else 0
        
        print(f"    Call Options Scanned: {call_count}")
        print(f"    Put Options Scanned:  {put_count}")
        print(f"    Put/Call Ratio:       {ratio:.2f}")
        
        if ratio > 1.0:
            print("    👉 Sentiment: BEARISH (High Demand for Puts)")
        elif ratio < 0.7:
            print("    👉 Sentiment: BULLISH (High Demand for Calls)")
        else:
            print("    👉 Sentiment: NEUTRAL")
            
    print("\n-------------------------------------------")

if __name__ == "__main__":
    analyze_data()