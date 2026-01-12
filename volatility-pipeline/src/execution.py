from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, OptionLegRequest, GetOptionContractsRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, OrderClass, PositionIntent, AssetStatus, ContractType
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import OptionLatestQuoteRequest
import sys
import datetime
import config 

class AlpacaTrader:
    def __init__(self):
        self.client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
        self.data_client = OptionHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
        print(f"✅ CONNECTED TO ALPACA (PAPER - MULTI-LEG ENABLED)")

    def get_positions(self):
        try: return self.client.get_all_positions()
        except: return []

    def close_position(self, symbol, reason):
        print(f"   📉 CLOSING {symbol}: {reason}")
        try: self.client.close_position(symbol)
        except Exception as e: print(f"   ❌ Close Failed: {e}")

    def get_next_friday(self):
        today = datetime.date.today()
        days_ahead = 4 - today.weekday()
        if days_ahead <= 0: days_ahead += 7
        return today + datetime.timedelta(days=days_ahead)

    def fetch_option_chain(self, symbol, expiration):
        try:
            req = GetOptionContractsRequest(underlying_symbols=[symbol], status=AssetStatus.ACTIVE, expiration_date=expiration, limit=10000)
            res = self.client.get_option_contracts(req)
            return res.option_contracts
        except: return []

    def select_contract(self, chain, strike, option_type):
        target_type = ContractType.CALL if option_type == 'call' else ContractType.PUT
        filtered = [c for c in chain if c.type == target_type]
        if not filtered: return None
        return min(filtered, key=lambda x: abs(float(x.strike_price) - strike)).symbol

    def get_mid_price(self, symbol):
        try:
            req = OptionLatestQuoteRequest(symbol_or_symbols=[symbol])
            res = self.data_client.get_option_latest_quote(req)
            quote = res[symbol]
            return (quote.bid_price + quote.ask_price) / 2
        except: return 0.0

    def submit_order(self, ticker, strikes, qty=1):
        print(f"\n--- 🦅 PREPARING IRON CONDOR: {ticker} ---")
        expiry = self.get_next_friday()
        chain = self.fetch_option_chain(ticker, expiry)
        
        sym_sp = self.select_contract(chain, strikes['sp'], 'put')
        sym_lp = self.select_contract(chain, strikes['lp'], 'put')
        sym_sc = self.select_contract(chain, strikes['sc'], 'call')
        sym_lc = self.select_contract(chain, strikes['lc'], 'call')

        if not (sym_sp and sym_lp and sym_sc and sym_lc):
            print("   ❌ Missing legs. Aborting.")
            return

        p_sp = self.get_mid_price(sym_sp)
        p_lp = self.get_mid_price(sym_lp)
        p_sc = self.get_mid_price(sym_sc)
        p_lc = self.get_mid_price(sym_lc)
        
        credit = (p_sp + p_sc) - (p_lp + p_lc)
        limit_price = round(credit * -1, 2) 
        print(f"   🎯 TARGET CREDIT: ${credit:.2f} (Limit: {limit_price})")

        legs = [
            OptionLegRequest(symbol=sym_lp, ratio_qty=1, side=OrderSide.BUY, position_intent=PositionIntent.BUY_TO_OPEN),
            OptionLegRequest(symbol=sym_sp, ratio_qty=1, side=OrderSide.SELL, position_intent=PositionIntent.SELL_TO_OPEN),
            OptionLegRequest(symbol=sym_sc, ratio_qty=1, side=OrderSide.SELL, position_intent=PositionIntent.SELL_TO_OPEN),
            OptionLegRequest(symbol=sym_lc, ratio_qty=1, side=OrderSide.BUY, position_intent=PositionIntent.BUY_TO_OPEN)
        ]

        try:
            req = LimitOrderRequest(
                symbol=None, 
                order_class=OrderClass.MLEG, 
                limit_price=float(limit_price), 
                time_in_force=TimeInForce.DAY, 
                qty=qty, 
                legs=legs
            )
            self.client.submit_order(req)
            print(f"   🚀 ORDER SENT: {ticker}")
        except Exception as e:
            print(f"   ❌ Order Rejected: {e}")
