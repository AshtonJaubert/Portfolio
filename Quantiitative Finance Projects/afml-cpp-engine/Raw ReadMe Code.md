# **High-Performance AFML Feature Engine (C++17)**

A low-latency, production-grade C++ implementation of key algorithms from Marcos López de Prado’s **"Advances in Financial Machine Learning"** (AFML). This engine is optimized for high-frequency trading  environments where deterministic performance and sub-microsecond latency are critical.

## ** Performance Benchmarks (Verified on Apple Silicon)**

| Feature | Median Latency | Throughput | Speedup vs. Python |
| :---- | :---- | :---- | :---- |
| **Triple-Barrier Labeling** | **33 ns** | **30.1 Million events/sec** | **\~100x** |
| **FracDiff (Window=256)** | **237 ns** | **4.2 Million events/sec** | **\~9x** |

*Benchmarks conducted using 1,000,000 mock ticks with O3 optimization.*

## ** Key Features**

* **Symmetric CUSUM Filter:** Efficient event-based sampling to identify significant price changes while filtering out noise.  
* **Triple-Barrier Labeling:** Deterministic labeling logic for training meta-labeling models, accounting for profit-taking, stop-loss, and time-out barriers.  
* **Fixed-Width Fractional Differentiation (FFD):** Stationarizes price series while preserving maximum memory, utilizing pre-computed binomial weights for ![][image1] efficiency.  
* **Zero-Allocation Architecture:** Uses stack-allocated circular buffers and std::array to eliminate heap-related jitter and ensure deterministic P99 latency.  
* **Data-Oriented Design:** Optimized for L1/L2 cache locality to maximize CPU throughput.

## ** Project Structure**

afml-cpp-engine/  
├── include/  
│   └── afml\_engine.hpp     \# Core header-only engine logic  
├── src/  
│   └── main.cpp            \# Simulation entry point  
├── tests/  
│   ├── test\_afml.cpp       \# Unit tests for labeling & CUSUM  
│   └── test\_fracdiff.cpp   \# Unit tests for FFD math  
├── benchmarks/  
│   ├── bench\_afml.cpp      \# C++ performance test suite  
│   └── comparison\_bench.py \# Python/NumPy baseline comparison  
└── Makefile                \# Clang build automation

## ** Build & Usage**

This project is optimized for MacOS using clang++ but is compatible with any C++17 compiler.

### **Build All Targets**

make

### **Run Tests**

./test\_suite     \# Basic engine logic  
./test\_frac      \# Fractional differentiation math

### **Run Performance Benchmarks**

./bench\_suite

### **Run Python Baseline (Requires NumPy)**

python3 benchmarks/comparison\_bench.py

## ** Technical Deep Dive: Why 33ns?**

The engine achieves sub-100ns latency by adhering to HFT systems programming principles:

1. **No Memory Allocation in the Hot Path:** By using a pre-allocated Ring Buffer (Circular Buffer) for active positions, we avoid the overhead of std::deque or std::vector reallocations.  
2. **Compile-Time Optimizations:** Utilizing C++ templates for buffer sizes allows the compiler to unroll loops and optimize memory offsets.  
3. **Branch Minimization:** The code is structured to keep the "Hot Path" (the tick-processing loop) as lean as possible, reducing branch mispredictions.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAYCAYAAAC8/X7cAAACu0lEQVR4Xu2Wy2sTURTGo61iFQU3BpKYyUsCWUghC19QqYIK4kZciuKi0I1uxMefULrqQmj/B0EEN+JK3ehGEBFEhS5ExHctaquNVL8znoknX0+SgRlBpD+4pPf7zuPeye2dZDKr/GeUy+VDrCWhVCoNsxYbLCYoFoszQRBcqdVqW9hn0Gwc4zLrSUH/n6z1BIuYkiQs/pTMK5VKEfO3GN84NqJarW6H/4r1CHjvpWY0HH/W+hhPjVfGmLPx3VgryVj4HTYEeD8wllkXJA8b38C6BXWvI+6BLnAP+2AQ+hMWBehfkX+M9Q608CzrEfAO6AYPkr4X47vVPCS30Wis1z5L7KPuWehHWRcKhcIOyWO9DcyXPQN+E35DGFetiHkrztlH3Lx+trTXIPmv7ZyRnFwut5F1OfP7dWG32bPgCW3VuE9WFw1PaMhqDC6EnYg7L3+jzj7JQd+7NkY31RXtPcl6+4nEOMMntcjDSKvX65v7NRYQcw0fA2YudTryML9n5wzWdyvwjqpXzAMFnulGxyMN89E4uRyDGhPaN/xWpGa/d4he6Z29cP1ti7sBLw6Nz7DmEej5J61dD59v2GewgUterwEttMiGBcknJI6vWGzgtFfUgphhxFxgHdpjye17wyhSw43TDaw0DN1isLjdnm6BfyNDN46QzWY3ad35Ev1De+DhTbu9pIBrKEh8IX6z2VzneOHNxLqllw9vWTcxyh6DXjcRt8B6iBTBU3jk6O8wWqxbJFdeUKwLaHpON7CGPQE9j/TaoEXXOMV6m+DP75X7GIuasIvjGM0JbxOD/Cz4jPFRxwJqHaaYEHgfWPOQPvKNs54YFL2I4l9YT5N8Pl+QDbCeGlp8xT9qWqD+HMZx1lNDz/Jz1tMAL7hs0Od3UiqgySSO0xjrSfmrR4eRFxtrScDTH2FtlX+JX/D/4+jN2UHmAAAAAElFTkSuQmCC>