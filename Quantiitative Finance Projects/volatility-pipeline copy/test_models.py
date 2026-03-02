import unittest
import os
import sys

# --- PATH SETUP ---
# Ensure we can find the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class TestVolatilityPipeline(unittest.TestCase):
    
    def test_0_dependencies(self):
        """CHECK 1: Are libraries installed?"""
        print("\n--- Checking Dependencies ---")
        try:
            import pandas
            import yfinance
            import alpaca
            import plotly
            import sqlalchemy
            print("✅ All required libraries found.")
        except ImportError as e:
            self.fail(f"❌ Missing Library: {e}. Did you run 'pip install -r requirements.txt'?")

    def test_1_structure(self):
        """CHECK 2: Are the files in the right place?"""
        print("\n--- Checking File Structure ---")
        required_files = [
            'config.py',
            'auto_trader.py',
            'src/strategy.py',
            'src/analytics.py',
            'src/execution.py'
        ]
        
        for f in required_files:
            path = os.path.join(current_dir, f)
            if not os.path.exists(path):
                self.fail(f"❌ Missing File: {f}")
            else:
                print(f"✅ Found {f}")

    def test_2_config(self):
        """CHECK 3: Is config valid?"""
        print("\n--- Checking Config ---")
        try:
            import config
            if not hasattr(config, 'PORTFOLIO'):
                self.fail("❌ Config missing 'PORTFOLIO' list.")
            print(f"✅ Config loaded. Trading {len(config.PORTFOLIO)} assets.")
        except Exception as e:
            self.fail(f"❌ Config Error: {e}")

    def test_3_strategy_logic(self):
        """CHECK 4: Does the Backtest run?"""
        print("\n--- Checking Strategy Logic ---")
        try:
            from src.strategy import run_ticker_backtest
            import config
            
            # Test on just one ticker to be fast
            test_ticker = config.PORTFOLIO[0]
            print(f"   Running quick test on {test_ticker}...")
            
            result = run_ticker_backtest(test_ticker)
            
            if result is None:
                print("⚠️ Backtest returned None (Data issue?), but code didn't crash.")
            else:
                print(f"✅ Backtest finished. Return: {result['Total Profit']:.2f}")
                
        except Exception as e:
            self.fail(f"❌ Strategy Crashed: {e}")

if __name__ == '__main__':
    unittest.main()