# Ashton Jaubert's Portfolio

Hello! This repository contains a collection of projects demonstrating my expertise in **MLOps**, **Quantitative Finance**, **Machine Learning**, and **Data Analytics**.

I specialize in building production-ready pipelines and applying mathematical models to solve economic and financial problems.

If you have any questions or feedback, I would be happy to connect on [LinkedIn](https://www.linkedin.com/in/ashtonjaubert/).

---

## 🛠 Skills & Tools

* **Languages:** Python, SQL, JavaScript
* **MLOps & Engineering:** Docker, DVC, FastAPI, Git, VS Code
* **Machine Learning:** Scikit-Learn, XGBoost, Scikit-Surprise, OpenCV
* **Financial Engineering:** Monte Carlo Simulations, Black-Scholes, Binomial Option Pricing
* **Data Analysis:** Pandas, NumPy, Tableau, Seaborn

---

## 🚀 MLOps & Machine Learning

### 🎬 MLOps Recommendation System (Collaborative Filtering)
* **Description:** A complete end-to-end MLOps pipeline for a movie recommendation engine. The system trains an SVD (Singular Value Decomposition) model and serves real-time predictions via a REST API.
* **Key Features:**
    * **API Serving:** Built a **FastAPI** microservice to serve predictions.
    * **Reproducibility:** Managed data and model versioning using **DVC**.
    * **Containerization:** Fully Dockerized application for consistent deployment across environments.
    * **Performance:** Achieved an RMSE of 0.935 on the MovieLens dataset.
* **Files:** [app.py](https://github.com/AshtonJaubert/Portfolio/blob/main/mlops-recommender-dvc/app.py) | [Dockerfile](https://github.com/AshtonJaubert/Portfolio/blob/main/mlops-recommender-dvc/Dockerfile)

### 🏠 Housing Loan Approval Prediction
* **Description:** A supervised learning project predicting loan approval status based on applicant features (Credit Score, Dependents, Loan Amount).
* **Key Achievement:** Developed **XGBoost** and **Random Forest** models achieving **98%+ accuracy**.
* **File:** [LoanApproval.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/LoanApproval.ipynb))

---
## 📜 Economic Research & Policy Analysis

### 🎓 Rural-Urban Disparities in Student Achievement
* **Description:** An econometric study analyzing the academic performance gap between students in rural and non-rural environments. The project investigates the socioeconomic factors contributing to educational inequality.
* **Methodology:**
    * **Stata Analysis:** Utilized Stata to clean data and perform statistical modeling.
    * **Regression Models:** Implemented regression analysis to isolate variables affecting student outcomes and quantify the rural-urban gap.
* **Files:** [Research Paper (PDF)](https://github.com/AshtonJaubert/Portfolio/blob/main/Rural-Urban-Disparities/Research_paper.pdf) | [Stata Script (.do)](https://github.com/AshtonJaubert/Portfolio/blob/main/Rural-Urban-Disparities/FInalProjectDO.do)

---


## 📈 Quantitative Finance & Financial Modeling

### Portfolio Optimization (Sharpe Ratio)
* **Description:** Utilized Python and `scipy.optimize` to construct an optimized investment portfolio. The model calculates optimal asset weights to maximize the Sharpe Ratio, balancing risk and return.
* **File:** [PortfolioOptimization.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/PorfolioOptimization.ipynb)

### Monte Carlo VaR & CVaR Analysis
* **Description:** Performed risk management analysis by calculating Value at Risk (VaR) and Conditional Value at Risk (CVaR) using Monte Carlo simulations.
* **File:** [MonteCarloVaRandCVar.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/MonteCarloVaRandCVar.ipynb)

### Option Pricing Models (Black-Scholes & Binomial)
* **Description:** Implemented two fundamental valuation models for financial derivatives using Python.
    * **Black-Scholes:** Calculated Call/Put prices using the BSM formula.
    * **Binomial Tree:** Priced options using discrete time-steps and risk-neutral probabilities.
* **Files:** [Black-ScholesModel.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/Black-ScholesModel.ipynb) | [BinomialOptionPricingModel.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/BinomialOptionPricingModel.ipynb)

### NVIDIA vs. Tech Market Analysis
* **Description:** A comparative market analysis assessing NVIDIA's volatility and historical returns against Microsoft, Apple, and the Nasdaq (QQQ).
* **File:** [NVIDIAMarketAnalysis.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/NVIDIAMarketAnalysis.ipynb)

---

## 📊 Data Analysis & Visualization

### Card Transaction EDA
* **Description:** Analyzed spending patterns from over 50,000 transactions. Created an interactive Tableau dashboard to showcase insights across gender, category, and location.
* **Links:** [Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/CardTransactions.ipynb) | [Tableau Dashboard](https://public.tableau.com/app/profile/ashton.jaubert/viz/TransactionDataAnalysis_17097954017460/Dashboard1)

### Balance of Trade (SQL)
* **Description:** Analyzed import and export data for 100+ countries (1960–2021) using MySQL. Utilized complex subqueries and aggregate functions to identify global trade deficits.
* **File:** [Imports&Exports.sql](https://github.com/AshtonJaubert/Portfolio/blob/main/Imports%26Exports.sql)

