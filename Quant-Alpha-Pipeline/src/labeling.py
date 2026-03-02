import pandas as pd
import numpy as np

def get_daily_vol(close, span0=100):
    df0 = close.index.searchsorted(close.index - pd.Timedelta(days=1))
    df0 = df0[df0 > 0]
    df0 = pd.Series(close.index[df0 - 1], index=close.index[close.shape[0] - df0.shape[0]:])
    df0 = close.loc[df0.index] / close.loc[df0.values].values - 1
    return df0.ewm(span=span0).std()

def apply_triple_barrier(close, events, pt_sl):
    out = events[['t1']].copy(deep=True)
    pt = pt_sl[0] * events['trgt'] if pt_sl[0] > 0 else pd.Series(index=events.index)
    sl = -pt_sl[1] * events['trgt'] if pt_sl[1] > 0 else pd.Series(index=events.index)

    for loc, t1 in events['t1'].fillna(close.index[-1]).items():
        path = close[loc:t1]
        returns = (path / close[loc] - 1) * events.at[loc, 'side']
        out.loc[loc, 'sl'] = returns[returns < sl[loc]].index.min()
        out.loc[loc, 'pt'] = returns[returns > pt[loc]].index.min()
    return out

def get_bins(barrier_hits, close):
    out = barrier_hits.copy(deep=True)
    for loc, row in barrier_hits.iterrows():
        first_hit = min(row.fillna(close.index[-1]))
        if row['pt'] == first_hit: out.loc[loc, 'bin'] = 1
        elif row['sl'] == first_hit: out.loc[loc, 'bin'] = -1
        else: out.loc[loc, 'bin'] = 0
    return out

def get_concurrency(bar_start, bar_end, close_index):
    num_concur = pd.Series(0, index=close_index)
    for start, end in zip(bar_start, bar_end):
        num_concur.loc[start:end] += 1
    return num_concur

def get_sample_uniqueness(bar_start, bar_end, num_concur):
    # bar_start is the index (DatetimeIndex), so we use it directly
    uniqueness = pd.Series(index=bar_start, dtype=float)
    for i in range(len(bar_start)):
        start, end = bar_start[i], bar_end.iloc[i]
        # Calculate the average uniqueness over the life of the barrier
        uniqueness.iloc[i] = (1.0 / num_concur.loc[start:end]).mean()
    return uniqueness