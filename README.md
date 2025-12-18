# Ashton Jaubert's Portfolio

Hello! This repository contains a collection of projects demonstrating my expertise in **Financial Modeling**, **Machine Learning**, **Data Analytics**, and **Software Development**. 

I have a strong focus on applying quantitative methods to economics and finance, utilizing tools like Python, SQL, and Tableau to drive insights.

If you have any questions or feedback, I would be happy to connect on [LinkedIn](https://www.linkedin.com/in/ashtonjaubert/).

---

## 🛠 Skills & Tools

* **Languages:** Python, SQL, JavaScript
* **Machine Learning:** Scikit-Learn, XGBoost, OpenCV, Predictive Modeling
* **Financial Engineering:** Monte Carlo Simulations, Black-Scholes, Binomial Option Pricing, VaR/CVaR Analysis
* **Data Analysis:** Pandas, NumPy, SciPy, Matplotlib, Seaborn
* **Web & Dev Tools:** React, Node.js, Git, Docker, VS Code

---

## 📈 Quantitative Finance & Financial Modeling

### Portfolio Optimization (Sharpe Ratio)
* **Description:** Utilized Python and `scipy.optimize` to construct an optimized investment portfolio. The model calculates optimal asset weights to maximize the Sharpe Ratio, balancing risk and return.
* **Key Features:** Automated ticker data download (YFinance), calculation of expected returns and volatility, and mathematical optimization.
* **File:** [PortfolioOptimization.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/PorfolioOptimization.ipynb)

### Monte Carlo VaR & CVaR Analysis
* **Description:** Performed risk management analysis by calculating Value at Risk (VaR) and Conditional Value at Risk (CVaR) using Monte Carlo simulations.
* **Key Features:** Comparison of Historical, Normal, t-distribution, and Monte Carlo methods to estimate potential portfolio losses.
* **File:** [MonteCarloVaRandCVar.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/MonteCarloVaRandCVar.ipynb)

### Option Pricing Models (Black-Scholes & Binomial)
* **Description:** Implemented two fundamental valuation models for financial derivatives.
    * **Black-Scholes:** Calculated Call and Put option prices using the classic BSM formula and `scipy.stats`.
    * **Binomial Tree:** Built a custom function to price options using discrete time-steps, accounting for up/down factors and risk-neutral probabilities.
* **Files:** * [Black-ScholesModel.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/Black-ScholesModel.ipynb)
    * [BinomialOptionPricingModel.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/BinomialOptionPricingModel.ipynb)

### NVIDIA vs. Tech Market Analysis
* **Description:** A comparative market analysis assessing NVIDIA's performance against major tech competitors (Microsoft, Apple) and the Nasdaq (QQQ).
* **Key Features:** Volatility analysis and historical return comparisons to determine investment viability.
* **File:** [NVIDIAMarketAnalysis.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/NVIDIAMarketAnalysis.ipynb)

---

## 🤖 Machine Learning & Computer Vision

### Housing Loan Approval Prediction
* **Description:** A supervised learning project predicting loan approval status based on applicant features (Credit Score, Dependents, Loan Amount).
* **Key Achievement:** Developed **XGBoost** and **Random Forest** models achieving **98%+ accuracy**.
* **Libraries:** Scikit-Learn, XGBoost, Pandas, Seaborn.
* **File:** [LoanApproval.ipynb](https://github.com/AshtonJaubert/Portfolio/blob/main/LoanApproval.ipynb)
* **Dataset:** [Kaggle](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset/data)

### ⚽️ Soccer Video Analysis System
* **Description:** An advanced computer vision application developed in Python to analyze soccer game footage. The system accurately tracks player and ball movements, assigns teams, and calculates key performance metrics.
* **Technologies:** Python, OpenCV, NumPy.
* **Key Features:**
    * **Object Detection & Tracking:** Custom-built tracker for players and the ball.
    * **Team Assignment:** Automated system to assign teams based on jersey color.
    * **Camera Movement Correction:** Algorithms to correct camera motion for accurate positioning.
    * **Performance Metrics:** Real-time calculation of player speed and distance covered.

---

## 📊 Data Analysis & Visualization

### Card Transaction EDA
* **Description:** Analyzed spending patterns from over 50,000 transactions across different genders, categories, and states. Created an interactive Tableau dashboard to showcase insights.
* **Links:** [Notebook](https://github.com/AshtonJaubert/Portfolio/blob/main/CardTransactions.ipynb) | [Tableau Dashboard](https://public.tableau.com/app/profile/ashton.jaubert/viz/TransactionDataAnalysis_17097954017460/Dashboard1)
* **Dataset:** [Kaggle](https://www.kaggle.com/datasets/rajatsurana979/comprehensive-credit-card-transactions-dataset/data)

### Balance of Trade (SQL)
* **Description:** Analyzed import and export data for 100+ countries (1960–2021) using SQL.
* **Techniques:** Utilized complex subqueries and aggregate functions (SUM, AVG, MAX) to identify global trade deficits and trends.
* **RDBMS:** MySQL.
* **File:** [Imports&Exports.sql](https://github.com/AshtonJaubert/Portfolio/blob/main/Imports%26Exports.sql)
* **Dataset:** [OurWorldinData.org](https://ourworldindata.org/economic-growth)

### Global GDP Tableau Dashboard
* **Description:** Interactive dashboard tracking Global GDP values from 1950–2019. Features filter tabs for specific years and countries to visualize economic fluctuations.
* **Link:** [View Dashboard](https://public.tableau.com/shared/G78HPBJ2X?:display_count=n&:origin=viz_share_link)
