import pandas as pd
import numpy as np
from sklearn.model_selection import KFold

class PurgedKFold:
    """
    Implements Purged K-Fold Cross-Validation
    Deletes samples from the training set that overlap with the test set.
    """
    def __init__(self, n_splits=3, pct_embargo=0.01):
        self.n_splits = n_splits
        self.pct_embargo = pct_embargo

    def split(self, X, y=None, groups=None, t1=None):
        """
        t1: Series where index is start time and value is end time of the barrier.
        """
        if t1 is None:
            raise ValueError("t1 (barrier end times) is required for purging.")
            
        kf = KFold(n_splits=self.n_splits, shuffle=False)
        indices = np.arange(X.shape[0])
        
        for train_indices, test_indices in kf.split(X):
            # 1. Identify test times
            test_t1 = t1.iloc[test_indices]
            test_start = test_t1.index[0]
            test_end = test_t1.max()
            
            # 2. PURGING
            relevant_train_indices = []
            for idx in train_indices:
                bar_start = t1.index[idx]
                bar_end = t1.iloc[idx]
                
                # If the training bar overlaps with the test period, purge it
                if not (bar_end < test_start or bar_start > test_end):
                    continue
                
                # 3. EMBARGO
                embargo_period = int(len(X) * self.pct_embargo)
                if bar_start > test_end and idx < test_indices[-1] + embargo_period:
                    continue
                    
                relevant_train_indices.append(idx)
            
            yield np.array(relevant_train_indices), test_indices