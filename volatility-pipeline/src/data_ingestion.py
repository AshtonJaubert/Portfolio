import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import sys
import os
import time

# --- IMPORT CONFIG CORRECTLY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def get_next_monthly_expiry(dates):
    """Finds the expiration date closest to 30-45 days out (Standard Logic)."""
    target = datetime.now() + timedelta(days=30)
    
    # Convert strings to datetime objects if needed
    dt_dates = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in dates]
    
    # Find closest date to target
    closest_date = min(dt_dates, key=lambda d: abs(d - target))
    return closest_date.strftime('%Y-%m-%d')

def fetch_and_store_data():
    print(f"--- 📥 STARTING INGESTION: {len(config.PORTFOLIO)} ASSETS ---")
    
    # Connect to Database
    db_path = os.path.join(os.path.dirname(__file__), '..', config.DB_NAME)
    connection_str = f"sqlite:///{db_path}"
    engine = create_engine(connection_str)
    
    for ticker in config.PORTFOLIO:
        attempts = 0
        max_retries = 3
        success = False
        
        while attempts < max_retries and not success:
            try:
                print(f"   Fetching {ticker} (Attempt {attempts+1})...")
                stock = yf.Ticker(ticker)
                
                # Get expirations
                exps = stock.options
                if not exps:
                    print(f"   ⚠️ {ticker}: No options found.")
                    break
                
                # Smart Selection: Target ~30-45 days out
                target_date = get_next_monthly_expiry(exps)
                
                # Fetch Calls and Puts
                opt = stock.option_chain(target_date)
                calls = opt.calls; calls['Type'] = 'Call'
                puts = opt.puts; puts['Type'] = 'Put'
                
                # Merge
                df = pd.concat([calls, puts])
                df['capture_timestamp'] = datetime.now()
                df['ticker'] = ticker
                df['expiration_date'] = target_date
                
                # Save to DB
                df.to_sql('options_history', engine, if_exists='append', index=False)
                print(f"   ✅ {ticker}: Saved {len(df)} rows (Exp: {target_date})")
                success = True
                
            except Exception as e:
                print(f"   ❌ Error {ticker}: {e}")
                attempts += 1
                time.sleep(2) # Wait before retry

    print(f"\n--- INGESTION COMPLETE ---")

if __name__ == "__main__":
    fetch_and_store_data()