#include <iostream>
#include <vector>
#include <chrono>
#include "afml_engine.hpp"

/**
 * High-Performance Benchmark: FracDiff + Triple Barrier
 * Measures the computational cost of maintaining stationarity.
 */

int main() {
    const int num_ticks = 1000000;
    std::vector<double> prices;
    prices.reserve(num_ticks);
    for(int i=0; i < num_ticks; ++i) {
        prices.push_back(100.0 + (i % 100) * 0.01);
    }

    // Window size of 256 is the "Standard" for daily data/high-memory features
    FracDiffEngine<256> frac_engine(0.3); 
    
    std::cout << "Benchmarking FracDiff (Window=256) over 1M ticks..." << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    for(double p : prices) {
        double stationarity_price = frac_engine.update(p);
        // Prevent compiler from optimizing away the loop
        if(stationarity_price < 0) std::cout << "Error" << std::endl; 
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << "------------------------------------------" << std::endl;
    std::cout << "Total Time: " << diff.count() / 1e6 << " ms" << std::endl;
    std::cout << "Latency per FracDiff Calc: " << diff.count() / num_ticks << " ns" << std::endl;
    std::cout << "Throughput: " << (double)num_ticks / (diff.count() / 1e9) / 1e6 << " M ticks/sec" << std::endl;
    std::cout << "------------------------------------------" << std::endl;

    return 0;
}