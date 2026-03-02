import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_expanded_performance():
    # 1. Load the expanded test results
    try:
        df = pd.read_csv('Final_resultsSPY.csv', index_col=0, parse_dates=True)
    except FileNotFoundError:
        print("Error: Final_resultsSPY.csv not found. Run main.py first.")
        return

    # 2. Parameters
    COST_PER_TRADE = 0.0005 # 5 basis points

    # 3. Returns Calculation
    # Price is already log-price from main.py
    df['market_returns'] = df['Price'].diff()
    
    # Shift signals to avoid look-ahead bias
    df['raw_signal'] = df['Model_Prediction'].shift(1)
    
    # Calculate transaction costs
    df['trades'] = df['raw_signal'].diff().fillna(0).abs()
    df['transaction_costs'] = df['trades'] * COST_PER_TRADE
    
    # Strategy Returns
    df['Strategy_Returns'] = (df['raw_signal'] * df['market_returns']) - df['transaction_costs']
    
    # 4. Cumulative Performance
    df['Cumulative_Market'] = df['market_returns'].fillna(0).cumsum().apply(np.exp)
    df['Cumulative_Strategy'] = df['Strategy_Returns'].fillna(0).cumsum().apply(np.exp)

    # 5. Plotting
    plt.figure(figsize=(12, 7))
    plt.plot(df['Cumulative_Market'], label='SPY Benchmark', color='gray', alpha=0.5, linestyle='--')
    plt.plot(df['Cumulative_Strategy'], label='AFML Strategy (Expanded Features)', color='teal', linewidth=2)
    
    # Formatting
    plt.title('Performance with Expanded Features (Volume & VIX Context)', fontsize=14, fontweight='bold')
    plt.ylabel('Growth of $1')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Metrics
    sharpe = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()) * np.sqrt(252) if df['Strategy_Returns'].std() != 0 else 0
    total_ret = (df['Cumulative_Strategy'].iloc[-1] - 1) * 100
    
    stats_text = f"Total Return: {total_ret:.2f}%\nAnn. Sharpe: {sharpe:.2f}\nTop Feature: Log_Volume"
    plt.gca().text(0.02, 0.85, stats_text, transform=plt.gca().transAxes, 
                   bbox=dict(facecolor='white', alpha=0.8), fontsize=10)

    plt.tight_layout()
    plt.savefig('expanded_performance_SPY.png')
    print("Plot saved as 'expanded_performance_SPY.png'")
    plt.show()

if __name__ == "__main__":
    plot_expanded_performance()