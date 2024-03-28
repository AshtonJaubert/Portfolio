#### In this Project I will be using a dataset that contains several companies across numerous years with specific values such as total assets and liabilities to create a supervised Machine Learning Model to predict a companies bankruptcy.

## Why is this Important?
With these models, companies can monitor how healthy their current company stands and if is at risk at bankruptcy.

Predicting bankruptcy is a critical task in finance, as it provides stakeholders with the chance to preemptively address potential financial setbacks. In recent years, extensive research has focused on employing machine learning techniques to forecast bankruptcy, utilizing financial ratios as key indicators.

## The Data 
The Data used for this Project is found on [Kaggle](https://www.kaggle.com/datasets/utkarshx27/american-companies-bankruptcy-prediction-dataset/data)

The software that was used in this Project is KNIME 

The values Used in these Models are:
- Current assets
- Cost of goods sold
- Depreciation and amortization
- EBITDA: Earnings before interest, taxes, depreciation, and amortization
- Inventory
- Net Income
- Total Assets
- Total Long-term Debt
- Total Current Liabilities
- Retained Earnings
- Total Liabilities

Types of ML Models used:
- Random forest
- Decision Tree
- Gradient Boosted Trees
- Tree Ensemble
- Logistic Regression
## The Results
I created a report containing the Data Workflow, The bankruptcy status totals, and the scores of each model with assigned heatmaps for each one.

You can find the report [here](https://github.com/AshtonJaubert/Portfolio/blob/main/Bankruptcy%20ML%20Project/ML_Report.pdf)
  
 You can also find the workflow [here](https://hub.knime.com/-/spaces/-/~QFBj6pZc3i1rjR66/)

## Conclusion
From the results of the report, all the models posted an accuracy score above 90%

The best Performing models were the Random Forest and the Decision Tree with accuracy scores just above 94%

The worst performing models were Logistic Regression and Gradient Boosted Trees with accuracy scores just above 93%

These models can be confidently implemented when used for checking company status if you are a company owner, as well as anticipating risk as a shareholder.


