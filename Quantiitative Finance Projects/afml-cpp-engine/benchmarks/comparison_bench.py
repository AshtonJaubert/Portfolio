import numpy as np
import time

def get_weights_ffd(d, length):
    """
    Standard AFML Weight calculation for FFD.
    Matches the binomial logic in your C++ engine.
    """
    w = [1.0]
    for k in range(1, length):
        w_k = -w[-1] / k * (d - k + 1)
        w.append(w_k)
    return np.array(w)

def python_frac_diff_benchmark(data, d, window=256):
    """
    Implements a sliding window dot-product in Python.
    This mimics exactly what the C++ update() loop does.
    """
    weights = get_weights_ffd(d, window)
    # We flip weights to align with the dot product against historical data
    weights = weights[::-1] 
    
    n = len(data)
    output = np.zeros(n - window)
    
    start_time = time.perf_counter()
    
    # This loop is the 'Hot Path' that C++ optimizes
    for i in range(window, n):
        # Slice the window
        chunk = data[i-window:i]
        # Perform Dot Product
        output[i-window] = np.dot(weights, chunk)
        
    end_time = time.perf_counter()
    return (end_time - start_time)

if __name__ == "__main__":
    num_ticks = 1000000
    print(f"Generating {num_ticks:,} mock ticks...")
    mock_data = np.random.normal(100, 1, num_ticks)
    
    print("Running Python Benchmark (Window Size: 256)...")
    duration_sec = python_frac_diff_benchmark(mock_data, 0.3)
    
    total_ms = duration_sec * 1000
    avg_ns_per_tick = (duration_sec / num_ticks) * 1e9
    throughput_m_sec = (num_ticks / duration_sec) / 1e6
    
    print("\n" + "="*40)
    print("PYTHON (NumPy) PERFORMANCE RESULTS")
    print("="*40)
    print(f"Total Time:         {total_ms:.2f} ms")
    print(f"Avg Latency/Tick:   {avg_ns_per_tick:,.0f} ns")
    print(f"Throughput:         {throughput_m_sec:.2f} Million ticks/sec")
    print("="*40)
    
    print("\nINSTRUCTIONS FOR COMPARISON:")
    print("1. Compare the 'Avg Latency/Tick' above with your C++ output (33ns - 237ns).")
    print("2. Divide Python Latency by C++ Latency to find the Speedup Factor.")