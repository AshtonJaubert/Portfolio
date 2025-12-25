# **Volatility Pipeline: Automated Iron Condor Backtester**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge&logo=amazon-aws)

## **📖 Project Overview**
The **Volatility Pipeline** is an end-to-end quantitative research framework designed to ingest financial data, analyze volatility regimes, and backtest defined-risk options strategies.

[cite_start]The system implements a **Relative Value Volatility Analysis (RVVA)** methodology[cite: 4]. [cite_start]It ingests real-time option data to calculate a "Fear Gauge" (Volatility Percentile) and systematically executes **Iron Condors** only when statistical edge is highest (Top 20% Volatility)[cite: 8]. [cite_start]The pipeline includes a "Reality Check" stress test that accounts for slippage and insurance costs (buying protective wings)[cite: 9, 10, 11].

## **🚀 Key Features**
* **Modular Architecture:** Separation of concerns between Data Ingestion (`data_ingestion.py`), Analytics (`analytics.py`), and Strategy execution (`strategy.py`).
* **Volatility Hunting Logic:** Automatically calculates a 20-day rolling volatility rank to determine if volatility is "Cheap" or "Expensive" before trading.
* [cite_start]**Defined-Risk Engine:** Converts theoretical Short Strangles into Iron Condors by buying 10% OTM wings to cap tail risk[cite: 5].
* **Persistent Storage:** Uses `SQLAlchemy` and `SQLite` to maintain a local ledger of option chains and trade history.
* [cite_start]**Automated Reporting:** Generates equity curves, calculates Sharpe Ratios, and identifies "Green Zone" vs. "Red Zone" assets[cite: 34, 42].

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