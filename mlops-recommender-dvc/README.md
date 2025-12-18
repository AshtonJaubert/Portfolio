# 🎬 MLOps Recommendation System

A production-ready recommendation engine built with **Python**, **FastAPI**, and **MLOps** best practices. This project demonstrates an end-to-end machine learning pipeline that trains a Collaborative Filtering model (SVD) and serves real-time predictions via a REST API.

## 🚀 Key Features
* **Machine Learning:** Implements the **SVD (Singular Value Decomposition)** algorithm using the `scikit-surprise` library to predict user ratings.
* **API Serving:** Deploys the model as a microservice using **FastAPI** for low-latency inference.
* **Reproducibility:** Uses **DVC (Data Version Control)** to manage the training pipeline and track data/model versions.
* **Containerization:** Fully containerized with **Docker**, ensuring consistency across development and production environments.

## 🛠 Tech Stack
* **Language:** Python 3.11
* **ML Libraries:** Scikit-Surprise, Pandas, Scikit-Learn
* **API Framework:** FastAPI, Uvicorn
* **Ops & Tools:** Docker, DVC, Joblib

## 📊 Model Performance
The model was trained on the MovieLens 100k dataset.
* **RMSE (Root Mean Square Error):** 0.935
* **MAE (Mean Absolute Error):** 0.738

## ⚙️ How to Run Locally

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/AshtonJaubert/Portfolio.git
cd mlops-recommender-dvc
pip install -r requirements.txt
