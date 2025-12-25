#  Ashton Jaubert's Portfolio

**Data Analyst | MLOps Engineer | Quantitative Finance Enthusiast**

Hello! Welcome to my portfolio. This repository hosts a collection of projects demonstrating my expertise in **MLOps**, **Quantitative Finance**, **Machine Learning**, and **Economic Research**.

I specialize in building production-ready pipelines and applying complex mathematical models to solve real-world economic and financial problems.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ashtonjaubert/)

---

## 🛠 Skills & Tools

| Domain | Tech Stack |
| :--- | :--- |
| **Languages** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **MLOps & Cloud** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat&logo=amazonaws&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![DVC](https://img.shields.io/badge/DVC-945DD6?style=flat&logo=dvc&logoColor=white) |
| **Machine Learning** | ![Scikit-Learn](https://img.shields.io/badge/scikitlearn-F7931E?style=flat&logo=scikit-learn&logoColor=white) ![NLTK](https://img.shields.io/badge/NLTK-2E7D32?style=flat&logo=python&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-EB4034?style=flat&logo=xgboost&logoColor=white) |
| **Data Viz** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) ![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat&logo=tableau&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) ![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=flat&logo=powerbi&logoColor=black) |
---

## 📈 Quantitative Finance (Featured)

### 📉 [Volatility Pipeline: Automated Iron Condor Backtester](https://github.com/AshtonJaubert/Portfolio/tree/main/VolatilityPipeline)
> **End-to-end quantitative research framework for defined-risk volatility trading.**

* **Description:** A Python-based pipeline that ingests option data, calculates a "Fear Gauge" (Vol Rank), and systematically executes **Iron Condors** only during high-volatility regimes (RVVA). It features a **"Reality Check"** engine that stress-tests strategies against slippage and insurance costs.
* **Research Findings (Reality Check):**
    The strategy was backtested under "Live Trading" conditions (assuming 40% premium reduction for slippage).
    | Ticker | Asset Class | Verdict | Sharpe | Return |
    | :--- | :--- | :--- | :--- | :--- |
    | **SPYI** | High Income ETF | 🏆 **Holy Grail** | **7.80** | **+27.00%** |
    | **SPY** | S&P 500 | ✅ Perfect | 7.26 | +23.22% |
    | **TSM** | Semiconductors | ✅ Production Ready | 3.85 | +12.67% |
    | **TSLA** | EV/Momentum | ❌ **Untradeable** | -4.09 | -41.79% |
* **Key Insights:**
    * **Compound Alpha:** **SPYI** outperformed **SPY** by applying the volatility filter on top of an existing yield strategy.
    * **The Cost of Safety:** Buying protective wings for **NVDA** reduced returns by ~75% compared to undefined-risk strategies (Strangle), highlighting the cost of tail-risk insurance.
    * **Momentum Risk:** **TSLA** failed due to "Gamma explosions" where price velocity exceeded short strikes faster than Theta decay could compensate.
* **Tech Stack:** Python, SQLite, SQLAlchemy, Pandas, Matplotlib, AWS (Roadmap).
* **Code:** [View Project](https://github.com/AshtonJaubert/Portfolio/tree/main/VolatilityPipeline)

### 🌍 [MarketPulse: Global Sentiment Analyzer](https://github.com/AshtonJaubert/Portfolio/tree/main/MarketPulse)
> **Full-stack NLP application for tracking international market sentiment.**

* **Description:** A serverless application that scrapes financial news from multiple regions, translates foreign headlines, and performs sentiment analysis to gauge global market mood.
* **Project Highlights:**
    * **Multi-Region Pipeline:** Aggregates real-time news from the **US (FinViz)**, **Mexico**, and **Taiwan (Google News)**, automatically translating Spanish and Mandarin headlines to English.
    * **NLP Sentiment Engine:** Utilizes **NLTK VADER** to score headlines on a -1 (Bearish) to +1 (Bullish) scale and classify market trends.
    * **Serverless Architecture:** Backend built with **FastAPI** and containerized using **Docker** for deployment on **AWS Lambda**.
    * **Interactive Dashboard:** Frontend developed in **Streamlit** featuring dynamic **Plotly** gauge charts to visualize live sentiment metrics.
* **Tech Stack:** Python, FastAPI, Docker, AWS Lambda, Streamlit, NLTK
* **Code:** [View Project](https://github.com/AshtonJaubert/Portfolio/tree/main/MarketPulse)

### [Portfolio Optimization (Sharpe Ratio)](https://github.com/AshtonJaubert/Portfolio/blob/main/PorfolioOptimization.ipynb)
* **Description:** Utilized `scipy.optimize` to calculate optimal asset weights that maximize the Sharpe Ratio, effectively balancing risk and return.
* **Code:** [View Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/PorfolioOptimization.ipynb)

### [Monte Carlo VaR & CVaR Analysis](https://github.com/AshtonJaubert/Portfolio/blob/main/MonteCarloVaRandCVar.ipynb)
* **Description:** Risk management analysis calculating Value at Risk (VaR) and Conditional Value at Risk (CVaR) via Monte Carlo simulations.
* **Code:** [View Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/MonteCarloVaRandCVar.ipynb)

### [Option Pricing Models (Black-Scholes & Binomial)](https://github.com/AshtonJaubert/Portfolio/blob/main/Black-ScholesModel.ipynb)
* **Description:** Implementation of fundamental derivative valuation models.
    * **Black-Scholes:** Calculated Call/Put prices using the BSM formula.
    * **Binomial Tree:** Priced options using discrete time-steps and risk-neutral probabilities.
* **Code:** [Black-Scholes](https://github.com/AshtonJaubert/Portfolio/blob/main/Black-ScholesModel.ipynb) | [Binomial Model](https://github.com/AshtonJaubert/Portfolio/blob/main/BinomialOptionPricingModel.ipynb)

### [NVIDIA vs. Tech Market Analysis](https://github.com/AshtonJaubert/Portfolio/blob/main/NVIDIAMarketAnalysis.ipynb)
* **Description:** Comparative analysis assessing NVIDIA's volatility and historical returns against Microsoft, Apple, and the Nasdaq (QQQ).
* **Code:** [View Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/NVIDIAMarketAnalysis.ipynb)

---

## 🚀 MLOps & Machine Learning

### 🎬 [MLOps Recommendation System (Collaborative Filtering)](https://github.com/AshtonJaubert/Portfolio/tree/main/mlops-recommender-dvc)
> **End-to-end MLOps pipeline serving real-time predictions.**

* **The Build:** Trains an SVD model and serves predictions via a **FastAPI** microservice.
* **Key Features:**
    * **Reproducibility:** Managed data/model versioning with **DVC**.
    * **Containerization:** Fully **Dockerized** for consistent deployment.
    * **Performance:** Achieved RMSE of **0.935** on MovieLens dataset.
* **Code:** [app.py](https://github.com/AshtonJaubert/Portfolio/blob/main/mlops-recommender-dvc/app.py) | [Dockerfile](https://github.com/AshtonJaubert/Portfolio/blob/main/mlops-recommender-dvc/Dockerfile)

### 🏠 [Housing Loan Approval Prediction](https://github.com/AshtonJaubert/Portfolio/blob/main/LoanApproval.ipynb)
* **Description:** Supervised learning project predicting loan approval status based on applicant metrics (Credit Score, Dependents, Loan Amount).
* **Performance:** Developed **XGBoost** and **Random Forest** models achieving **98%+ accuracy**.
* **Code:** [View Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/LoanApproval.ipynb)

---

## 📜 Economic Research & Policy Analysis

### 🎓 [Rural-Urban Disparities in Student Achievement](https://github.com/AshtonJaubert/Portfolio/blob/main/Rural-Urban-Disparities/Research_paper.pdf)
> **An econometric study on educational inequality.**

* **Objective:** Investigated socioeconomic factors contributing to the performance gap between rural and non-rural students.
* **Methodology:**
    * **Stata Analysis:** Cleaned large datasets and performed statistical modeling.
    * **Regression Models:** Isolated variables affecting outcomes to quantify the rural-urban gap.
* **Read:** [Research Paper (PDF)](https://github.com/AshtonJaubert/Portfolio/blob/main/Rural-Urban-Disparities/Research_paper.pdf) | [Stata Script (.do)](https://github.com/AshtonJaubert/Portfolio/blob/main/Rural-Urban-Disparities/FInalProjectDO.do)

---

## 📊 Data Analysis & Visualization

### [Card Transaction EDA](https://public.tableau.com/app/profile/ashton.jaubert/viz/TransactionDataAnalysis_17097954017460/Dashboard1)
* **Description:** Analyzed spending patterns from 50,000+ transactions. Created an interactive Dashboard to showcase insights across gender, category, and location.
* **View:** [Tableau Dashboard](https://public.tableau.com/app/profile/ashton.jaubert/viz/TransactionDataAnalysis_17097954017460/Dashboard1) | [Jupyter Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/CardTransactions.ipynb)

### [Balance of Trade (SQL)](https://github.com/AshtonJaubert/Portfolio/blob/main/Imports%26Exports.sql)
* **Description:** Analyzed import/export data for 100+ countries (1960–2021) using **MySQL**. Used complex subqueries and aggregates to identify global trade deficits.
* **Code:** [SQL Script](https://github.com/AshtonJaubert/Portfolio/blob/main/Imports%26Exports.sql)
