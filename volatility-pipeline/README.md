# **Volatility Pipeline: Automated Iron Condor System**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?style=for-the-badge&logo=amazon-aws)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Alpaca](https://img.shields.io/badge/Alpaca-Trading%20API-yellow?style=for-the-badge&logo=alpacadotmarkets)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

## **📖 Project Overview**
The **Volatility Pipeline** is a full-stack algorithmic trading system hosted on AWS. It is designed to identify "expensive" volatility regimes and systematically execute **Iron Condors** to capture option premium.

Unlike simple backtesters, this system is a **Live Trading Bot** that:
1.  **Ingests Data:** Fetches real-time market data to calculate a "Fear Gauge" (Volatility Percentile).
2.  **Analyzes Regimes:** Uses a 20-day rolling volatility rank to determine entry signals (Entry > 75th Percentile).
3.  **Executes Multi-Leg Orders:** Uses the Alpaca API to submit atomic Iron Condor orders (4 legs simultaneously) to minimize leg-in risk.
4.  **Visualizes Performance:** Features a live "Institutional Trading Desk" dashboard built with Streamlit.

[![Launch Dashboard](https://img.shields.io/badge/🚀_Launch-Live_Dashboard-success?style=for-the-badge)](http://13.58.237.61:8501)

---

## **📂 Project Structure**
This repository is organized into modular components for data, logic, and execution.

```bash
volatility-pipeline/
├── auto_trader.py          # 🤖 MAIN BOT: The live loop that scans markets & trades 24/7
├── Dashboard.py            # 📊 UI: Streamlit Dashboard for monitoring the bot
├── config.py               # 🔑 CONFIG: API Keys, Portfolio list, and Settings
├── requirements.txt        # 📦 DEPS: Python libraries (alpaca-py, streamlit, etc.)
├── main.py                 # 🏁 ENTRY: Alternate entry point for the pipeline
├── test_models.py          # 🧪 TESTS: Unit tests for DB connections and logic
├── quant.db                # 💾 DATA: SQLite database for option chain history
│
└── src/
    ├── execution.py        # 🦅 EXECUTION: Handles Alpaca "Multi-Leg" order submission
    ├── strategy.py         # 🧠 BACKTESTER: Simulates strategy performance on historical data
    ├── analytics.py        # 📈 ANALYSIS: Calculates Volatility Rank & Aggressive sizing logic
    └── data_ingestion.py   # 📥 ETL: Fetches raw option chains for offline research
