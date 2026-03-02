import sys
import os

# Ensure Python can find the 'src' modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the functions from your source files
try:
    from src.data_ingestion import fetch_and_store_data
    from src.analytics import analyze_data
    from src.strategy import run_backtest
    import config
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you are running this from the root directory (volatility-pipeline).")
    sys.exit(1)

def main():
    print("=======================================================")
    print(f"   🚀 VOLATILITY PIPELINE: {len(config.PORTFOLIO)} ASSETS")
    print(f"   Mode: Ingestion -> Analytics -> Strategy Backtest")
    print("=======================================================")

    # --- STEP 1: INGESTION ---
    # Downloads live options chains for the whole portfolio to build your database
    print("\n>>> [Step 1/3] Starting Data Ingestion...")
    try:
        fetch_and_store_data()
    except Exception as e:
        print(f"❌ CRITICAL ERROR during ingestion: {e}")
        # We exit here because if we have no data, the other steps are useless
        sys.exit(1) 

    # --- STEP 2: ANALYTICS ---
    # Scans the portfolio to tell you what is "Expensive" (Trade) or "Cheap" (Wait)
    print("\n>>> [Step 2/3] Running Institutional Analytics...")
    try:
        analyze_data()
    except Exception as e:
        print(f"❌ ERROR during analytics: {e}")
        # Proceeding anyway because analytics is just for reporting

    # --- STEP 3: STRATEGY BACKTEST ---
    # Runs the "2022 Bear Market Test" to verify your math holds up
    print("\n>>> [Step 3/3] Running Strategy Validation (Backtest)...")
    try:
        run_backtest()
    except Exception as e:
        print(f"❌ ERROR during strategy execution: {e}")

    print("\n=======================================================")
    print("   ✅ PIPELINE COMPLETE")
    print("=======================================================")

if __name__ == "__main__":
    main()