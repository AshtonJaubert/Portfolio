import pandas as pd
import numpy as np
import datetime
import sys
import os
import time
import logging
import pytz  # <--- NEW: For Timezone conversion
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from src.execution import AlpacaTrader
import config

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# --- SETTINGS ---
CHECK_INTERVAL_SECONDS = 900 
VOL_LOOKBACK = 20
VOL_PERCENTILE_THRESHOLD = 0.75
TARGET_PORTFOLIO_VOL = 0.20
TAKE_PROFIT_PCT = 0.80
STOP_LOSS_PCT = -0.85

def is_market_open():
    """
    Checks if the market is currently open.
    User requested: 8:35 AM CT start. 
    Market closes: 3:00 PM CT (4:00 PM ET).
    """
    # 1. Define New York Timezone
    ny_tz = pytz.timezone('America/New_York')
    now_ny = datetime.datetime.now(ny_tz)
    
    # 2. Check Day of Week (0=Mon, 4=Fri)
    if now_ny.weekday() > 4:
        logger.info(f"   💤 Market Closed (Weekend)")
        return False

    # 3. Check Time (9:35 AM ET to 4:00 PM ET)
    # 9:35 ET = 8:35 CT (Texas)
    # 16:00 ET = 3:00 PM CT (Texas)
    market_start = now_ny.replace(hour=9, minute=35, second=0, microsecond=0)
    market_end = now_ny.replace(hour=16, minute=0, second=0, microsecond=0)

    if market_start <= now_ny <= market_end:
        return True
    else:
        logger.info(f"   💤 Market Closed (Current NY Time: {now_ny.strftime('%H:%M')})")
        return False

def manage_exits(broker):
    logger.info("--- 💼 MANAGING EXITS ---")
    positions = broker.get_positions()
    if not positions:
        logger.info("   No open positions.")
        return

    for p in positions:
        try:
            pl_pct = float(p.unrealized_plpc)
            symbol = p.symbol
            logger.info(f"   {symbol}: {pl_pct:.2%}")
            
            if pl_pct >= TAKE_PROFIT_PCT:
                broker.close_position(symbol, f"Take Profit (+{pl_pct:.1%})")
                logger.info(f"   📉 CLOSING {symbol}: Take Profit")
            elif pl_pct <= STOP_LOSS_PCT:
                broker.close_position(symbol, f"Stop Loss ({pl_pct:.1%})")
                logger.info(f"   📉 CLOSING {symbol}: Stop Loss")
            else:
                logger.info(f"   -> HOLD (Target +{TAKE_PROFIT_PCT:.0%})")
                
        except Exception as e:
            logger.error(f"   Error checking {p.symbol}: {e}")

def get_strategy_signal(ticker, current_equity):
    try:
        data_client = StockHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
        
        # Free Plan Fix: Ask for data ending 20 mins ago
        end_dt = datetime.datetime.now() - datetime.timedelta(minutes=20)
        start_dt = end_dt - datetime.timedelta(days=365)
        
        req = StockBarsRequest(
            symbol_or_symbols=[ticker],
            timeframe=TimeFrame.Day,
            start=start_dt,
            end=end_dt
        )
        
        bars = data_client.get_stock_bars(req)
        if bars.df.empty: return None

        df = bars.df.loc[ticker].copy()
        
        df['returns'] = df['close'].pct_change()
        df['rolling_vol'] = df['returns'].rolling(VOL_LOOKBACK).std() * np.sqrt(252)
        
        if len(df) < VOL_LOOKBACK: return None

        current_vol = df['rolling_vol'].iloc[-1]
        vol_rank = (df['rolling_vol'] < current_vol).mean()
        price = df['close'].iloc[-1]

        if vol_rank > VOL_PERCENTILE_THRESHOLD:
            if current_vol > 0:
                vol_scaler = max(0.1, min(TARGET_PORTFOLIO_VOL / current_vol, 2.0))
            else:
                vol_scaler = 1.0
                
            allocation = current_equity * 0.05 * vol_scaler
            qty = max(1, int(allocation / price))
            
            strikes = {
                'sp': price * 0.96, 'lp': price * 0.90,
                'sc': price * 1.04, 'lc': price * 1.10
            }
            return {"signal": True, "vol_rank": vol_rank, "qty": qty, "strikes": strikes}
            
        return None

    except Exception as e:
        logger.error(f"   Error scanning {ticker}: {e}")
        return None

def run_cycle():
    logger.info("==========================================")
    logger.info(f"   🔎 SCANNING MARKETS: {datetime.datetime.now()}")
    logger.info("==========================================")
    
    try:
        broker = AlpacaTrader()
        account = broker.client.get_account()
        current_equity = float(account.equity)
    except Exception as e:
        logger.critical(f"❌ Connection Failed: {e}")
        return

    manage_exits(broker)

    logger.info("--- 🔭 SCANNING TARGETS ---")
    for ticker in config.PORTFOLIO:
        try:
            positions = broker.get_positions()
            holding = any(p.symbol == ticker for p in positions)
            if holding: continue

            signal = get_strategy_signal(ticker, current_equity)
            if signal:
                logger.info(f"   ✅ SIGNAL FOUND: {ticker}")
                logger.info(f"      Vol Rank: {signal['vol_rank']:.1%}")
                broker.submit_order(ticker, signal['strikes'], qty=signal['qty'])
        except Exception as e:
             logger.error(f"   Skipping {ticker}: {e}")

def start_bot():
    logger.info("   🚀 AWS STRATEGY BOT STARTED (Schedule: 9:35 AM - 4:00 PM ET)")
    while True:
        try:
            if is_market_open():
                run_cycle()
            else:
                pass # Just sleep if closed
        except Exception as e:
            logger.critical(f"❌ CRITICAL ERROR: {e}")
        
        logger.info(f"   💤 Sleeping for {CHECK_INTERVAL_SECONDS/60} mins...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
   start_bot()
