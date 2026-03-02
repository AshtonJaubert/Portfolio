from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import sys
import os
import config

class AlpacaTrader:
    def __init__(self):
        try:
            self.client = TradingClient(
                config.ALPACA_API_KEY,
                config.ALPACA_SECRET_KEY,
                paper=True
            )
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            raise e

    def get_positions(self):
        try:
            return self.client.get_all_positions()
        except:
            return []

    def close_position(self, symbol, reason):
        print(f"   📉 CLOSING {symbol}: {reason}")
        try:
            self.client.close_position(symbol)
        except Exception as e:
            print(f"   ❌ Close Failed: {e}")

    def submit_order(self, ticker, strikes, qty=1):
        """Submits a Market Order (Self-managed risk)."""
        
        # 1. Check if we already hold it
        positions = self.get_positions()
        for p in positions:
            if p.symbol == ticker:
                print(f"   ⚠️ SKIPPED: Already hold {ticker}")
                return

        # 2. Check Buying Power
        account = self.client.get_account()
        if float(account.buying_power) < 2000:
            print("   ⚠️ SKIPPED: Insufficient Buying Power")
            return

        print(f"   🤖 EXECUTING {ticker} (Condor Setup)")
        
        try:
            req = MarketOrderRequest(
                symbol=ticker,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            self.client.submit_order(req)
            print(f"   ✅ ORDER SENT: {ticker}")
            
        except Exception as e:
            print(f"   ❌ Execution Failed: {e}")