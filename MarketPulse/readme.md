# MarketPulse: Serverless Financial Sentiment API

**MarketPulse** is a lightweight, cloud-native API that provides real-time sentiment analysis for stock tickers. Instead of relying on delayed or expensive financial data feeds, it scrapes the latest news headlines directly from FinViz and uses Natural Language Processing (NLP) to generate immediate "Bullish" or "Bearish" trading signals.

Built with **FastAPI**, **Docker**, and **NLTK**, and designed for serverless deployment on **AWS Lambda**.

---

## 🚀 Features

* **Real-Time Data Extraction:** Custom-built scraper using `BeautifulSoup` and `Requests` to bypass unreliable third-party APIs.
* **NLP-Driven Insights:** Utilizes the **VADER** (Valence Aware Dictionary and Sentiment Reasoner) model to detect market sentiment from unstructured text.
* **Statistically Significant Sampling:** Analyzes the latest 30 headlines to balance statistical relevance with recency bias (avoiding stale news).
* **Serverless Architecture:** Wrapped with **Mangum** adapter and containerized with Docker, making it strictly compatible with AWS Lambda.

## 🛠️ Tech Stack

* **Framework:** Python 3.11, FastAPI
* **Data Acquisition:** Requests, BeautifulSoup4 (Web Scraping)
* **Machine Learning:** NLTK (VADER Sentiment Analysis)
* **Deployment:** Docker, AWS Lambda, Mangum (ASGI Adapter)

## ⚡ Quick Start (Local)

### Prerequisites
* Python 3.11+
* Docker (Optional, for container testing)

### 1. Installation
Clone the repository and install dependencies.

```bash
pip install -r requirements.txt
