import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import sys
import os
import time
from src.execution import AlpacaTrader
import config

# --- AWS SETTINGS ---
CHECK_INTERVAL_SECONDS = 900  # Check every 15 mins

# --- STRATEGY PARAMETERS (MATCHING STRATEGY.PY) ---
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.75  # Entry: Vol > 75%
TARGET_PORTFOLIO_VOL = 0.20      # Target Volatility
INITIAL_CAPITAL = 100000         # Base for sizing (Or fetch actual equity)

# --- EXIT RULES (MATCHING STRATEGY.PY) ---
TAKE_PROFIT_PCT = 0.80  # Close at +80% 
STOP_LOSS_PCT = -0.85   # Stop at -85%

def manage_exits(broker):
    """Checks open positions against Backtest Exit Rules."""
    print("\n--- 💼 MANAGING EXITS ---")
    positions = broker.get_positions()
    if not positions:
        print("   No open positions.")
        return

    for p in positions:
        try:
            # Calculate P/L
            pl_pct = float(p.unrealized_plpc)
            symbol = p.symbol
            
            print(f"   {symbol}: {pl_pct:.2%}")
            
            # EXIT LOGIC
            if pl_pct >= TAKE_PROFIT_PCT:
                broker.close_position(symbol, f"Take Profit (+{pl_pct:.2%})")
            elif pl_pct <= STOP_LOSS_PCT:
                broker.close_position(symbol, f"Stop Loss ({pl_pct:.2%})")
        except Exception as e:
            print(f"   Error managing {p.symbol}: {e}")

def get_strategy_signal(ticker, current_equity):
    """
    Applies the exact logic from strategy.py to generate 
    Entries, Sizing, and Strikes.
    """
    indices = getattr(config, 'INDICES', ['SPY', 'QQQ', 'IWM', 'DIA'])
    
    try:
        # 1. Fetch Data (Need enough history for ranking)
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty: return None
        
        if isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        
        # 2. Calculate Indicators
        df['returns'] = df[col].pct_change()
        df['rolling_vol'] = df['returns'].rolling(VOL_LOOKBACK).std() * np.sqrt(252)
        
        # Current Metrics
        current_price = df[col].iloc[-1]
        current_vol = df['rolling_vol'].iloc[-1]
        
        # Calculate Rank (Percentile of current vol vs last year)
        # We count how many days in the past had lower vol than today
        vol_rank = (df['rolling_vol'] < current_vol).mean()
        
        # 3. Check Entry Threshold 
        if vol_rank < VOL_PERCENTILE_THRESHOLD:
            return None # No Trade

        # 4. Define Strikes (Iron Condor)
        strikes = {
            'sp': current_price * 0.96, # Short Put
            'lp': current_price * 0.90, # Long Put
            'sc': current_price * 1.04, # Short Call
            'lc': current_price * 1.10  # Long Call
        }
        
        # 5. Calculate Sizing (The "Math")
        # Vol Scaler: Target / Current
        vol_scaler = max(0.1, min(TARGET_PORTFOLIO_VOL / current_vol, 2.0))
        
        # Aggressive Multiplier (The "Double Down")
        aggressive_multiplier = 1.0
        if vol_rank > 0.95:
            aggressive_multiplier = 2.0
            print(f"   🔥 EXTREME VOLATILITY ({vol_rank:.0%}) - DOUBLING SIZE")

        # Risk Calculation
        max_risk_per_share = (strikes['sp'] - strikes['lp']) # Spread width
        
        # Final Quantity Formula
        # qty = (Equity * Risk_Allocation * Scaler * Aggressive) / (Trade_Risk * 100)
        risk_allocation = 0.05 # 5% of account per trade
        
        qty = int((current_equity * risk_allocation * vol_scaler * aggressive_multiplier) / (max_risk_per_share * 100))
        qty = max(1, qty) # Always buy at least 1

        return {
            "ticker": ticker,
            "strikes": strikes,
            "qty": qty,
            "vol_rank": vol_rank,
            "debug_vol": current_vol
        }

    except Exception as e:
        print(f"   ❌ Error analyzing {ticker}: {e}")
        return None

def run_cycle():
    print(f"\n[{datetime.datetime.now()}] Starting Scan...")
    
    try:
        broker = AlpacaTrader()
        
        # Get Live Equity for Sizing
        account = broker.client.get_account()
        current_equity = float(account.equity)
        print(f"   💰 Buying Power: ${float(account.buying_power):,.2f} | Equity: ${current_equity:,.2f}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 1. Manage Exits (Priority)
    manage_exits(broker)

    # 2. Scan for New Trades
    print("\n--- 🔭 SCANNING TARGETS ---")
    for ticker in config.PORTFOLIO:
        
        # Skip if we already hold it
        positions = broker.get_positions()
        holding = any(p.symbol == ticker for p in positions)
        if holding:
            continue

        signal = get_strategy_signal(ticker, current_equity)
        
        if signal:
            print(f"   ✅ SIGNAL FOUND: {ticker}")
            print(f"      Vol Rank: {signal['vol_rank']:.1%} (Thresh: {VOL_PERCENTILE_THRESHOLD:.0%})")
            print(f"      Size: {signal['qty']} Units")
            
            # Execute
            broker.submit_order(ticker, signal['strikes'], qty=signal['qty'])
        else:
            # print(f"   . {ticker} (No Signal)") # Quiet Mode
            pass

def start_bot():
    print("==========================================")
    print("   🚀 AWS STRATEGY BOT STARTED")
    print(f"   Logic: Entry > {VOL_PERCENTILE_THRESHOLD:.0%} | TP {TAKE_PROFIT_PCT:.0%} | SL {STOP_LOSS_PCT:.0%}")
    print("==========================================")
    
    while True:
        try:
            run_cycle()
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
        
        print(f"   Sleeping for {CHECK_INTERVAL_SECONDS}s...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    start_bot()