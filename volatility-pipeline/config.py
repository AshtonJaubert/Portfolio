# --- DATABASE SETTINGS ---
DB_NAME = 'quant.db'
import os


# --- API KEYS ---

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "YOUR_API_KEY_HERE")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "YOUR_SECRET_KEY_HERE")

# --- STRATEGY SETTINGS ---
# Assets to trade
PORTFOLIO = ['SPY', 'QQQ', 'IWM', 'DIA', 'GLD', 'SLV', 'TLT', 'NVDA', 'TSLA']

# Indices 
INDICES = ['SPY', 'QQQ', 'IWM', 'DIA']

# Target Volatility for Portfolio Sizing
TARGET_TICKER = "SPY"  # Default watcher

