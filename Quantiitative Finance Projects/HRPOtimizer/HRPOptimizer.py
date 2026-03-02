import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram

class HRPOptimizer:
    """
    Complete HRP Optimizer with Backtesting and Benchmark Comparison.
    """
    
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.returns = None
        self.weights = None

    def download_data(self):
        """Fetch prices and handle the MultiIndex columns from yfinance."""
        print(f"Downloading data for: {self.tickers}...")
        raw_data = yf.download(self.tickers, start=self.start_date, end=self.end_date, auto_adjust=True)
        
        if raw_data.empty:
            raise ValueError("No data downloaded. Verify tickers or internet connection.")

        if isinstance(raw_data.columns, pd.MultiIndex):
            df = raw_data['Close']
        else:
            df = raw_data[['Close']]
            
        self.returns = df.pct_change().dropna()
        return self.returns

    def get_quasi_diag(self, link):
        """Matrix Seriation: Sorts the clusters so similar assets are adjacent."""
        link = link.astype(int)
        sort_ix = pd.Series([link[-1, 0], link[-1, 1]])
        num_items = link[-1, 3]
        
        while sort_ix.max() >= num_items:
            sort_ix.index = range(0, sort_ix.shape[0] * 2, 2)
            df0 = sort_ix[sort_ix >= num_items]
            i = df0.index
            j = df0.values - num_items
            sort_ix[i] = link[j, 0]
            df0 = pd.Series(link[j, 1], index=i + 1)
            sort_ix = pd.concat([sort_ix, df0])
            sort_ix = sort_ix.sort_index()
            sort_ix.index = range(sort_ix.shape[0])
            
        return sort_ix.tolist()

    def get_cluster_var(self, cov, cluster_items):
        """Compute the variance of a cluster using inverse-variance weights."""
        cov_slice = cov.loc[cluster_items, cluster_items]
        ivp = 1. / np.diag(cov_slice)
        ivp /= ivp.sum()
        w = ivp.reshape(-1, 1)
        cluster_var = np.dot(np.dot(w.T, cov_slice), w)[0, 0]
        return cluster_var

    def get_rec_bisection(self, cov, sort_ix):
        """Recursive bisection to assign weights based on cluster risk."""
        w = pd.Series(1.0, index=sort_ix)
        c_items = [sort_ix]
        
        while len(c_items) > 0:
            c_items = [i[j:k] for i in c_items for j, k in ((0, len(i) // 2), (len(i) // 2, len(i))) if len(i) > 1]
            for i in range(0, len(c_items), 2):
                c_items0 = c_items[i]
                c_items1 = c_items[i+1]
                
                var0 = self.get_cluster_var(cov, c_items0)
                var1 = self.get_cluster_var(cov, c_items1)
                
                alpha = 1 - var0 / (var0 + var1)
                w[c_items0] *= alpha
                w[c_items1] *= 1 - alpha
        return w

    def optimize(self):
        """Execute the HRP pipeline."""
        if self.returns is None:
            self.download_data()
            
        corr = self.returns.corr()
        cov = self.returns.cov()
        dist = np.sqrt(0.5 * (1 - corr))
        link = sch.linkage(dist, 'single')
        sort_ix_raw = self.get_quasi_diag(link)
        sort_ix = corr.index[sort_ix_raw].tolist()
        self.weights = self.get_rec_bisection(cov, sort_ix)
        return self.weights, link

    def run_backtest(self):
        """Compare HRP against an Equal Weight (1/N) benchmark."""
        if self.weights is None:
            print("Must run optimize() before backtesting.")
            return

        # 1. Calculate Portfolio Returns
        hrp_port_returns = (self.returns * self.weights).sum(axis=1)
        
        # 2. Calculate Benchmark Returns
        num_assets = len(self.returns.columns)
        ew_weights = np.repeat(1.0/num_assets, num_assets)
        ew_port_returns = (self.returns * ew_weights).sum(axis=1)
        
        # 3. Cumulative Growth (starting from $1)
        hrp_cum = (1 + hrp_port_returns).cumprod()
        ew_cum = (1 + ew_port_returns).cumprod()
        
        # 4. Visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot Returns
        hrp_cum.plot(ax=ax1, label='HRP Portfolio', color='navy', linewidth=2)
        ew_cum.plot(ax=ax1, label='Equal Weight (Benchmark)', color='gray', alpha=0.6, linestyle='--')
        ax1.set_title('Backtest: Growth of $1')
        ax1.set_ylabel('Cumulative Return')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot Drawdowns
        def get_drawdown(cum_rets):
            peaks = cum_rets.cummax()
            return (cum_rets - peaks) / peaks

        get_drawdown(hrp_cum).plot(ax=ax2, label='HRP Drawdown', color='red', kind='area', alpha=0.3)
        ax2.set_title('Portfolio Drawdowns')
        ax2.set_ylabel('Drawdown %')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

        # Summary Statistics
        print("\n--- Performance Metrics (Annualized) ---")
        hrp_vol = hrp_port_returns.std() * np.sqrt(252)
        ew_vol = ew_port_returns.std() * np.sqrt(252)
        print(f"HRP Volatility: {hrp_vol:.2%}")
        print(f"EW Volatility:  {ew_vol:.2%}")
        print(f"Risk Reduction: {((ew_vol - hrp_vol) / ew_vol):.2%} lower volatility than EW")

if __name__ == "__main__":
    # diversified set of assets
    assets = ['SPY', 'TLT', 'GLD', 'VNQ', 'AAPL', 'MSFT', 'XLE']
    
    # Run from 2020 to capture the COVID crash and recovery
    hrp = HRPOptimizer(assets, start_date='2020-01-01', end_date='2024-01-01')
    
    try:
        weights, link = hrp.optimize()
        
        print("\n--- HRP Optimized Weights ---")
        print(weights.sort_values(ascending=False))
        
        #Run the backtest comparison
        hrp.run_backtest()
        
    except Exception as e:
        print(f"Error: {e}")
