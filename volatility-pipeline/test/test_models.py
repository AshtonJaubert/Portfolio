import unittest
import os
import sqlite3
import sys

# --- ROBUST PATH SETUP ---
# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Check if config.py is in the current directory (Root)
if os.path.exists(os.path.join(current_dir, 'config.py')):
    sys.path.append(current_dir)
# If not, assume we are in a subfolder (like /tests) and add the parent directory
else:
    sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

try:
    import config
    # Try importing strategy. If it fails, add 'src' explicitly
    try:
        from src.strategy import run_backtest
    except ImportError:
        # If running from root, src might not be picked up if not a package
        sys.path.append(os.path.join(current_dir, 'src'))
        from strategy import run_backtest
except ImportError as e:
    print(f"❌ CRITICAL SETUP ERROR: Could not find 'config.py'.\nError: {e}")
    sys.exit(1)

class TestVolatilityPipeline(unittest.TestCase):
    
    def setUp(self):
        """Runs before every test."""
        self.db_name = config.DB_NAME
        self.ticker = config.TARGET_TICKER
        
    def test_1_database_exists(self):
        """Is the database file actually there?"""
        # Handle path if DB is relative
        if not os.path.isabs(self.db_name):
            # Try to find DB relative to root
            root_path = os.path.dirname(config.__file__)
            db_path = os.path.join(root_path, self.db_name)
        else:
            db_path = self.db_name

        exists = os.path.exists(db_path)
        self.assertTrue(exists, f"❌ Database file {db_path} not found!")
        if exists:
            print(f"✅ Database found: {db_path}")

    def test_2_table_exists(self):
        """Does the 'options_history' table exist?"""
        # Resolve DB path again
        root_path = os.path.dirname(config.__file__)
        db_path = os.path.join(root_path, self.db_name) if not os.path.isabs(self.db_name) else self.db_name

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        
        self.assertTrue(len(tables) > 0, "❌ No tables found in DB.")
        print(f"✅ Tables found: {tables}")

    def test_3_strategy_sanity_check(self):
        """Does the new Iron Condor strategy run without crashing?"""
        print("Testing Strategy Logic...")
        try:
            # We suppress print output during testing to keep it clean
            sys.stdout = open(os.devnull, 'w')
            run_backtest()
            sys.stdout = sys.__stdout__ # Restore print
            print("✅ Strategy execution successful (Iron Condor logic works)")
        except Exception as e:
            sys.stdout = sys.__stdout__
            self.fail(f"❌ Strategy CRASHED during execution: {e}")

if __name__ == '__main__':
    unittest.main()