import sys
import os

# Ensure Python can find the 'src' modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the functions from your source files
try:
    from src.data_ingestion import fetch_and_store_data
    from src.analytics import analyze_data
    from src.strategy import run_backtest  # <--- ADDED STRATEGY IMPORT
    import config
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you are running this from the root directory (volatility-pipeline).")
    sys.exit(1)

def main():
    print("========================================")
    print(f"   VOLATILITY PIPELINE: {config.TARGET_TICKER}")
    print("========================================")

    # --- STEP 1: INGESTION ---
    print("\n>>> [Step 1/3] Starting Data Ingestion...")
    try:
        fetch_and_store_data()
    except Exception as e:
        print(f"❌ CRITICAL ERROR during ingestion: {e}")
        sys.exit(1) # Stop if we can't get data

    # --- STEP 2: ANALYTICS ---
    print("\n>>> [Step 2/3] Starting Analytics...")
    try:
        analyze_data()
    except Exception as e:
        print(f"❌ ERROR during analytics: {e}")
        # We don't exit here because we might still want to run the strategy

    # --- STEP 3: STRATEGY BACKTEST ---
    print("\n>>> [Step 3/3] Running Strategy Backtest...")
    try:
        run_backtest()
    except Exception as e:
        print(f"❌ ERROR during strategy execution: {e}")

    print("\n========================================")
    print("   Pipeline Complete ✅")
    print("========================================")

if __name__ == "__main__":
    main()