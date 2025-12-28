# **Volatility Pipeline: Automated Iron Condor System**

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-Click_Here-success?style=for-the-badge&logo=streamlit)](http://13.58.237.61:8501/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![AWS](https://img.shields.io/badge/AWS-EC2%20%2F%20Lambda-orange?style=for-the-badge&logo=amazon-aws)
![Alpaca](https://img.shields.io/badge/Alpaca-Live%20Execution-yellow?style=for-the-badge&logo=alpaca)

## **📖 Project Overview**
The **Volatility Pipeline** is an institutional-grade quantitative trading framework designed to exploit mean-reversion in volatility. It hunts for "expensive fear" in the options market and systematically sells **Iron Condors** when statistical edge is maximized.

Unlike typical retail bots, this system implements a **Relative Value Volatility Analysis (RVVA)** engine. It calculates a "Fear Gauge" (20-Day Rolling Volatility Rank) for every asset in the portfolio. When volatility hits the **top 75th percentile**, the bot executes defined-risk spreads to capture premium, while automatically hedging tail risk.

The system is fully deployed on **AWS**, featuring a continuous trading loop and a real-time **Streamlit Dashboard** for P&L monitoring.

## **🚀 Key Features**
* **☁️ Cloud-Native Execution:** Runs 24/7 on AWS EC2/Lambda using `auto_trader.py`, ensuring zero downtime for market scans.
* **📊 Live Strategy Dashboard:** A `Streamlit` interface provides real-time visualization of Open Positions, P&L, Buying Power, and "Wait vs. Trade" zones.
* **🧠 Volatility Hunting Logic:**
    * **Entry:** Volatility Rank > 75% (Statistical Extremes).
    * **Sizing:** Dynamic position sizing based on Portfolio Volatility Target (20%).
    * **Execution:** Automated multi-leg ordering (Iron Condors) via Alpaca API.
* **🛡️ Risk Management Engine:**
    * **Active Management:** Automated profit taking at +80% and Stop Loss at -85%.
    * **Reality Check:** Accounts for slippage and "Wing Drag" (cost of protection).
* **💾 Persistent Ledger:** Uses `SQLite` for local trade logging and backtest data storage.

## **⚡ System Architecture**
The system is divided into three autonomous components:

| Component | File | Role |
| :--- | :--- | :--- |
| **The Manager** | `auto_trader.py` | Infinite loop that scans the market every 15 mins. It handles signal generation, risk checks, and submits orders to Alpaca. |
| **The Monitor** | `Dashboard.py` | A web-based GUI (hosted on port 8501) for human oversight. Connects to Alpaca in Read-Only mode to display equity curves. |
| **The Lab** | `main.py` | The research pipeline. Used for backtesting new hypotheses (e.g., "What if we trade only on Tuesdays?") without risking capital. |

## **🔬 Research Findings (2024 Market Test)**
The strategy was stress-tested against 2024 market data with strict active management rules (**Take Profit @ 80%** | **Stop Loss @ -85%**).

**Aggregate Performance:**
* **🏆 Total Profit:** $40,899.93 (100k buying power)
* **🎯 Win Rate:** 78.3%

| Ticker | Asset Class | Total Return | Sharpe Ratio | Max Drawdown | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **IWM** | Small Caps | **+5.8%** | **3.54** | -0.8% | 🏆 Best Risk/Reward |
| **TSLA** | EV/Momentum | **+7.7%** | **3.08** | -0.7% | 🚀 High Alpha |
| **GLD** | Gold | **+4.4%** | **3.16** | -0.3% | ✅ Safe Haven |
| **SPY** | S&P 500 | **+5.3%** | **2.52** | -0.7% | ✅ Consistent |
| **DIA** | Dow Jones | **+4.2%** | **2.64** | -0.5% | ✅ Stable |
| **QQQ** | Tech | **+4.2%** | **2.20** | -1.4% | ✅ Solid |
| **TLT** | Bonds | **+2.2%** | **2.71** | -0.3% | 🛡️ Low Vol Hedge |
| **SLV** | Silver | **+3.5%** | **1.33** | -1.7% | ⚠️ Lower Efficiency |

### **Critical Analysis & Insights**
* **The Tesla Redemption:** Previous versions of this algorithm failed on TSLA due to gamma risk. The new "Active Management" logic (Stop Loss @ -85%) successfully tamed the tail risk, turning TSLA into the highest grossing asset (+7.7%) with a surprisingly high Sharpe Ratio (3.08).
* **Small Cap Dominance:** IWM (Russell 2000) proved to be the ideal environment for this strategy (Sharpe 3.54), likely due to its mean-reverting nature in 2024 compared to the directional trend of Tech (QQQ).
* **Safety First:** The maximum drawdown across the entire portfolio never exceeded **1.7%** (SLV), proving the efficacy of the defined-risk Iron Condor structure combined with aggressive stop losses.

## **📂 Project Structure**
```bash
volatility-pipeline/
├── auto_trader.py          # 🤖 LIVE BOT: The infinite loop for AWS
├── Dashboard.py            # 📊 GUI: Streamlit Web Dashboard
├── config.py               # ⚙️ SETTINGS: API Keys & Portfolio targets
├── main.py                 # 🔬 LAB: Backtesting pipeline entry point
├── requirements.txt        # Dependencies (yfinance, alpaca-py, streamlit)
├── quant.db                # Database (SQLite)
├── src/
│   ├── data_ingestion.py   # ETL: Fetches option chains
│   ├── analytics.py        # Math: Calculates Vol Rank
│   ├── strategy.py         # Backtester Logic
│   └── execution.py        # Execution: Alpaca API Interface
└── reports/                # Generated performance charts
