import numpy as np
import pandas as pd

def get_weights_ffd(d, thres, width):
    
    w = [1.0]
    for k in range(1, width):
        w_ = -w[-1] / k * (d - k + 1)
        if abs(w_) < thres: 
            break
        w.append(w_)
    return np.array(w[::-1]).reshape(-1, 1)

def frac_diff_ffd(series, d, thres=1e-4):
    """
    Applies FFD to a pandas DataFrame.
    """
    w = get_weights_ffd(d, thres, len(series))
    width = len(w) - 1
    
    if width >= len(series):
        print(f"Warning: Window width {width} exceeds series length {len(series)} for d={d}")
        return pd.DataFrame()

    df = {}
    for name in series.columns:
        seriesF = series[name].ffill().dropna()
        vals = seriesF.values
        res = []
        # Vectorized-style loop for performance
        for i in range(width, len(vals)):
            res.append(np.dot(w.T, vals[i-width : i+1])[0])
        
        df[name] = pd.Series(res, index=seriesF.index[width:])
    return pd.DataFrame(df)