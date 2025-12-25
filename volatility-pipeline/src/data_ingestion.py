import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import sys
import os

# Allow importing from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

TICKER = config.TARGET_TICKER

def fetch_and_store_data():
    # --- NEW CODE: SQLite Connection ---
    print(f"Connecting to database at: {config.DB_NAME}")
    # sqlite:/// (3 slashes) means relative path, 4 slashes means absolute.
    # We use the absolute path we defined in config.py
    connection_str = f"sqlite:///{config.DB_NAME}"
    engine = create_engine(connection_str)
    # -----------------------------------
    
    print(f"Fetching data for {TICKER}...")
    stock = yf.Ticker(TICKER)
    
    try:
        target_date = stock.options[2]
    except IndexError:
        print("No options found.")
        return

    opt = stock.option_chain(target_date)
    calls = opt.calls
    calls['Type'] = 'Call'
    puts = opt.puts
    puts['Type'] = 'Put'
    
    df = pd.concat([calls, puts])
    df['capture_timestamp'] = datetime.now()
    df['ticker'] = TICKER
    df['expiration_date'] = target_date
    
    print(f"Writing {len(df)} rows to database...")
    
    # Write to SQLite
    # index=False prevents pandas from adding a weird 'index' column
    # New (Cleaner)
    df.to_sql('options_history', con=engine, if_exists='append', index=False)
    
    print("Success! Data saved to quant.db")

if __name__ == "__main__":
    fetch_and_store_data()