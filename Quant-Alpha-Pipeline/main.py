import pandas as pd
import numpy as np
import yfinance as yf
import os
import sys
from sklearn.metrics import classification_report

# Ensure imports work from src/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

try:
    from src.features import frac_diff_ffd
    from src.labeling import get_daily_vol, apply_triple_barrier, get_bins, get_concurrency, get_sample_uniqueness
    from src.models import AlphaModel
    from src.validation import PurgedKFold
except ImportError as e:
    print(f"IMPORT ERROR: {e}. Check your src/ folder.")
    sys.exit(1)

def run_pipeline():
    ticker = 'SPY'  # You can change this to 'SPY' or any other ticker
    print(f"--- STARTING TUNED OPTIMAL ALPHA PIPELINE ({ticker}) ---")

    # 1. DATA ACQUISITION
    print("Fetching SPY and VIX context...")
    raw_SPY = yf.download(ticker, start='2015-01-01', end='2025-01-01', auto_adjust=True)
    raw_vix = yf.download('^VIX', start='2015-01-01', end='2025-01-01', auto_adjust=True)
    
    if isinstance(raw_SPY.columns, pd.MultiIndex): raw_SPY.columns = raw_SPY.columns.get_level_values(0)
    if isinstance(raw_vix.columns, pd.MultiIndex): raw_vix.columns = raw_vix.columns.get_level_values(0)

    # 2. FEATURE ENGINEERING (Option A: Expansion)
    price_series = raw_SPY['Close']
    log_prices = np.log(raw_SPY[['Close']]).rename(columns={'Close': 'Price'})
    
    X = frac_diff_ffd(log_prices, d=0.3)
    X['Log_Volume'] = np.log(raw_SPY['Volume'].loc[X.index])
    X['VIX'] = raw_vix['Close'].loc[X.index]

    # 3. LABELING (Option B: 1:1 Ratio Tuning)
    print("Step 2: Generating Tuned Triple-Barrier labels (1:1 Ratio)...")
    vol = get_daily_vol(price_series)
    t_events = X.index 
    t1_idx = price_series.index.searchsorted(t_events + pd.Timedelta(days=20))
    t1_idx = t1_idx[t1_idx < price_series.shape[0]]
    t1_vertical = pd.Series(price_series.index[t1_idx], index=t_events[:len(t1_idx)])
    
    events = pd.concat({'t1': t1_vertical, 'trgt': vol, 'side': pd.Series(1, index=t1_vertical.index)}, axis=1).dropna()
    
    # We change pt_sl from [2, 1] to [1, 1] for the trending SPY regime
    raw_labels = apply_triple_barrier(price_series, events, pt_sl=[1, 1])
    
    # UNIQUENESS & ALIGNMENT
    end_times = raw_labels.min(axis=1).fillna(price_series.index[-1])
    concur = get_concurrency(events.index, end_times, price_series.index)
    uniqueness = get_sample_uniqueness(events.index, end_times, concur)
    y = get_bins(raw_labels, price_series)

    final_df = X.loc[X.index.intersection(y.index)].copy()
    final_df['label'] = y.loc[final_df.index, 'bin']
    final_df['uniqueness'] = uniqueness.loc[final_df.index]
    final_df['t1'] = end_times.loc[final_df.index]

    # 4. MACHINE LEARNING (Option C: Confidence Veto)
    model_engine = AlphaModel()
    X_ml, y_ml, sw_ml, t1_ml = model_engine.prepare_features(final_df)

    print("Running Purged K-Fold CV...")
    cv = PurgedKFold(n_splits=5, pct_embargo=0.01)
    cv_score = model_engine.cross_validate_purged(X_ml, y_ml, t1=t1_ml, cv_gen=cv, sample_weight=sw_ml)
    
    # Execute with 60% probability threshold for betting
    print("Executing Final Walk-Forward with 60% Confidence Veto...")
    y_test, primary_preds, final_signals, bet_sizes = model_engine.train_and_meta_label(
        X_ml, y_ml, sample_weight=sw_ml, prob_threshold=0.60
    )

    # 5. SAVE TEST RESULTS
    test_results = pd.DataFrame({
        'Price': X_ml.loc[y_test.index, 'Price'],
        'Model_Prediction': primary_preds, # These are now Vetoed (lots of 0s)
        'Bet_Size': bet_sizes
    }, index=y_test.index)
    
    test_results.to_csv('Final_resultsSPY.csv')
    print("\nTuned test results saved to 'Final_resultsSPY.csv'")

    # 6. FINAL REPORT
    print("\n" + "="*45)
    print("TUNED STRATEGY REPORT")
    print("="*45)
    print(f"Purged K-Fold CV Accuracy: {cv_score:.2%}")
    print(f"Strategy Activity (Betting %): {(primary_preds != 0).mean():.2%}")
    print(f"Top Predictive Features:")
    print(model_engine.get_feature_importance(X_ml.columns).head(3))
    

if __name__ == "__main__":
    run_pipeline()