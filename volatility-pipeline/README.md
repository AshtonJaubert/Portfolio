# **Volatility Pipeline: Automated Iron Condor Backtester**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge&logo=amazon-aws)

## **📖 Project Overview**
The **Volatility Pipeline** is an end-to-end quantitative research framework designed to ingest financial data, analyze volatility regimes, and backtest defined-risk options strategies.

he system implements a **Relative Value Volatility Analysis (RVVA)** methodology. It ingests real-time option data to calculate a "Fear Gauge" (Volatility Percentile) and systematically executes **Iron Condors** only when statistical edge is highest (Top 20% Volatility). The pipeline includes a "Reality Check" stress test that accounts for slippage and insurance costs (buying protective wings).

## **🚀 Key Features**
* **Modular Architecture:** Separation of concerns between Data Ingestion (`data_ingestion.py`), Analytics (`analytics.py`), and Strategy execution (`strategy.py`).
* **Volatility Hunting Logic:** Automatically calculates a 20-day rolling volatility rank to determine if volatility is "Cheap" or "Expensive" before trading.
* **Defined-Risk Engine:** Converts theoretical Short Strangles into Iron Condors by buying 10% OTM wings to cap tail risk.
* **Persistent Storage:** Uses `SQLAlchemy` and `SQLite` to maintain a local ledger of option chains and trade history.
* **Automated Reporting:** Generates equity curves, calculates Sharpe Ratios, and identifies "Green Zone" vs. "Red Zone" assets.
## **🔬 Research Findings & Reality Check**
The strategy was stress-tested under "Live Trading" conditions over a 1-year period. The following matrix details the performance after applying the **"Reality Gap"** constraints (assuming a 40% reduction in premium capture to account for slippage and wing costs).

| Ticker | Asset Class | Total Return | Sharpe Ratio | Max Drawdown | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SPYI** | High Income ETF | **+27.00%** | **7.80** | 0.00% | 🏆 The Holy Grail |
| **SPY** | S&P 500 | **+23.22%** | **7.26** | 0.00% | ✅ Perfect |
| **TSM** | Semiconductors | **+12.67%** | **3.85** | -2.96% | ✅ Production Ready |
| **NVDA** | AI/Tech | **+6.72%** | **1.90** | -6.30% | ⚠️ Viable (Low Yield) |
| **MSFT** | Tech | **+0.45%** | **0.26** | -17.57% | ⚠️ Inefficient |
| **TSLA** | EV/Momentum | **-41.79%** | **-4.09** | -42.19% | ❌ UNTRADEABLE |

### **Critical Analysis & Insights**
* **The "Compound Alpha" Discovery:** SPYI (NEOS S&P 500 High Income ETF) outperformed SPY (+27% vs +23%). By applying our volatility filter on top of their existing strategy, we created a "Compound Alpha" effect—trading a volatility product only during peak volatility windows.
* **The Cost of Safety ("Wing Drag"):** A comparative analysis on **NVDA** revealed the high cost of defined risk.
    * *Theory (Strangle):* Sharpe Ratio **4.8**
    * *Reality (Iron Condor):* Sharpe Ratio **1.9**
    * *Conclusion:* Buying protective wings reduced returns by ~75%. While necessary for safety, it makes single-stock volatility trading capital inefficient compared to indices.
* **Momentum Risk (The Tesla Case):** The strategy failed on **TSLA** (-41% return). Momentum-driven assets experience "Gamma explosions" where price velocity exceeds the short strikes faster than Theta decay can compensate.

## **🔮 Roadmap: Cloud & Real-Time Trading**
The next phase of this project focuses on moving from backtesting to forward-testing in a live environment.

* **☁️ AWS Deployment:**
    * Migrate the pipeline to **AWS EC2** or **AWS Lambda** to ensure 24/7 uptime and continuous data ingestion.
    * Automate the `main.py` execution using **AWS EventBridge** (Cron) to run daily market scans.
* **🔔 Discord Alerts:**
    * Integrate Discord Webhooks to broadcast real-time signals.
    * **Goal:** Receive an instant notification on my phone whenever the "Fear Gauge" (Vol Rank) crosses the 80% threshold, allowing for manual execution of the strategy.
* **📈 Forward Testing:**
    * Connect to a paper-trading API to track the "Reality Gap" in real-time execution versus the backtest model.

## **📂 Project Structure**
```bash

volatility-pipeline/
├── src/
│   ├── data_ingestion.py   # ETL: Fetches option chains & stores in SQLite
│   ├── analytics.py        # logic: Calculates Vol Rank & Put/Call Ratios
│   ├── strategy.py         # Engine: Simulates Iron Condor execution
│   └── __init__.py
├── reports/                # Generated performance charts (PNGs)
├── config.py               # Configuration (Target tickers, DB paths)
├── main.py                 # Pipeline entry point
├── research.ipynb          # Jupyter Notebook for comparative analysis
├── test_models.py          # Unit tests for DB connection & logic
├── quant.db                # SQLite database
└── requirements.txt        # Python dependencies
