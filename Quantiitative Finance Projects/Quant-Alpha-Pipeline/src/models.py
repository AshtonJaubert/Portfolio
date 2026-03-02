import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import norm
from sklearn.metrics import accuracy_score

class AlphaModel:
    def __init__(self, n_estimators=100, max_depth=5):
        self.primary_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42, class_weight='balanced')
        self.meta_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42, class_weight='balanced')

    def prepare_features(self, df, lags=5):
        X = df[['Price', 'VIX', 'Log_Volume']].copy()
        for i in range(1, lags + 1):
            X[f'Price_lag_{i}'] = df['Price'].shift(i)
        y = df['label']
        valid_data = pd.concat([X, y, df[['uniqueness', 't1']]], axis=1).dropna()
        return valid_data.drop(columns=['label', 'uniqueness', 't1']), valid_data['label'], valid_data['uniqueness'], valid_data['t1']

    def cross_validate_purged(self, X, y, t1, cv_gen, sample_weight=None):
        scores = []
        for train_idx, test_idx in cv_gen.split(X, t1=t1):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            sw_train = sample_weight.iloc[train_idx] if sample_weight is not None else None
            self.primary_model.fit(X_train, y_train, sample_weight=sw_train)
            preds = self.primary_model.predict(X_test)
            scores.append(accuracy_score(y_test, preds))
        return np.mean(scores)

    def train_and_meta_label(self, X, y, sample_weight=None, train_size=0.8, prob_threshold=0.60):
        split_idx = int(len(X) * train_size)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        sw_train = sample_weight.iloc[:split_idx] if sample_weight is not None else None
        
        # 1. Primary Model
        self.primary_model.fit(X_train, y_train, sample_weight=sw_train)
        test_preds = self.primary_model.predict(X_test)
        
        # 2. Meta-Labeling
        train_preds = self.primary_model.predict(X_train)
        y_meta_train = pd.Series(0, index=y_train.index)
        mask = train_preds != 0
        y_meta_train.loc[mask] = (train_preds[mask] == y_train[mask]).astype(int)
        
        # 3. Meta-Model
        self.meta_model.fit(X_train, y_meta_train, sample_weight=sw_train)
        meta_probs = self.meta_model.predict_proba(X_test)[:, 1]
        
        # --- NEW: VETO LOGIC ---
        # If meta_prob < threshold, we output a 0 (No Trade)
        veto_filter = (meta_probs >= prob_threshold).astype(int)
        
        # 4. Bet Sizing
        bet_sizes = (meta_probs - 0.5) / np.sqrt(meta_probs * (1 - meta_probs) + 1e-9)
        bet_sizes = pd.Series(2 * norm.cdf(bet_sizes) - 1, index=X_test.index)
        
        # Final Signal = Direction * Veto * Bet Size
        final_signal = test_preds * veto_filter * bet_sizes
        
        # return the vetoed prediction for visualization
        vetoed_preds = test_preds * veto_filter
        
        return y_test, vetoed_preds, final_signal, bet_sizes

    def get_feature_importance(self, feature_names):
        return pd.Series(self.meta_model.feature_importances_, index=feature_names).sort_values(ascending=False)