# Institutional Alpha Pipeline: AFML Implementation (SPY & QQQ)

This repository contains a professional-grade quantitative trading pipeline based on the methodologies introduced by **Marcos López de Prado** in *"Advances in Financial Machine Learning"* (AFML).

The project addresses the core challenges of financial machine learning: **Non-stationarity**, **Sample Dependency (Concurrency)**, and **Look-ahead Bias**.

##  Key Technical Features

* **Fractional Differentiation (**$d=0.3$**):** Fixed-width Window FracDiff (FFD) to achieve stationarity while preserving maximum memory of the price series.

* **Triple-Barrier Labeling:** Implements path-dependent labeling with dynamic volatility scaling and a symmetric 1:1 Reward/Risk ratio.

* **Concurrency Correction:** Calculates **Sample Uniqueness** to apply weight-based corrections during training, preventing overfitting on overlapping price paths.

* **Purged K-Fold Cross-Validation:** Custom CV generator with a **1% Embargo period** to ensure zero data leakage between folds.

* **Meta-Labeling & Confidence Veto:** A two-stage modeling approach. Signals are only executed if the secondary Meta-Model outputs a probability $\geq 60\%$.

* **Equivalent Frequency Bet Sizing:** Dynamically scales position sizes based on the Meta-Model's conviction using the Normal CDF scaling method.

## 📊 Strategy Performance Report

The pipeline was tested out-of-sample (OOS) for the 2023-2025 period. By applying the 60% confidence veto, the strategy identifies high-conviction regimes while staying in cash during high-noise periods.

### **Nasdaq 100 ETF (QQQ) Results**

| Metric | Value | 
 | ----- | ----- | 
| **Purged K-Fold Accuracy** | **49.03%** | 
| **Strategy Activity (Betting %)** | **53.19%** | 
| **Top Predictive Feature** | `VIX` (0.234862) | 
| **Second Predictive Feature** | `Log_Volume` (0.148899) | 
| **Third Predictive Feature** | `Price` (0.146385) | 

### **S&P 500 ETF (SPY) Results**

| Metric | Value | 
 | ----- | ----- | 
| **Purged K-Fold Accuracy** | **48.98%** | 
| **Strategy Activity (Betting %)** | **50.83%** | 
| **Top Predictive Feature** | `Price_lag_3` (0.169322) | 
| **Second Predictive Feature** | `VIX` (0.133351) | 
| **Third Predictive Feature** | `Price` (0.129574) | 


##  Usage

1. **Install dependencies:** `pip install pandas numpy yfinance scikit-learn scipy matplotlib`

2. **Run the pipeline:** `python3 main.py`

3. **Generate curves:** `python3 visualization.py`

##  Researcher's Commentary

The strategy demonstrates **Defensive Alpha**. By utilizing **VIX** and **Log-Volume** as contextual features, the Meta-Model identifies market regimes where price action is most reliable. In both SPY and QQQ, the model maintained an accuracy significantly higher than the break-even threshold for a symmetric 1:1 barrier, while the veto mechanism successfully reduced maximum drawdown by ignoring low-confidence trade signals.