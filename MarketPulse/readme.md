# 🌍 MarketPulse: Global Sentiment Analyzer

**MarketPulse** is a full-stack financial intelligence tool that provides real-time sentiment analysis for stock tickers across international markets. It combines a serverless **FastAPI** backend with an interactive **Streamlit** dashboard to scrape, translate, and analyze news headlines from the US, Mexico, and China/Taiwan.

Unlike standard tools that rely on expensive data feeds, MarketPulse scrapes live data from **FinViz** (for US stocks) and **Google News RSS** (for global stocks), automatically translating foreign headlines to English before performing NLP sentiment scoring.

---

## 📸 Dashboard Previews

| **US Market Analysis (USA)** | **Global Market Analysis (Mexico)** | **Global Market Analysis (China/Taiwan)**
|:---:|:---:|:---:|
| *Real-time bullish/bearish signals for US tickers.* | *Sentiment analysis for Spanish-language news.* | *Sentiment analysis for Mandarin-language news.* |
| ![US View](MarketPulse_App_USA.pdf) | ![Mexico View](MarketPulseGlobalMexico.pdf) | ![China View](MarketPulse_App_SS.pdf)

---

## 🚀 Key Features

* **🌎 Multi-Market Support:**
    * **US Market:** Scrapes FinViz for major US tickers (e.g., TSLA, NVDA).
    * **Global Markets:** Scrapes Google News for **Spanish (Mexico)** and **Mandarin (China/Taiwan)** headlines.
* **🗣️ Automated Translation Pipeline:** Integrates `deep-translator` to detect foreign headlines and translate them to English on-the-fly for accurate VADER analysis.
* **📊 Interactive Dashboard:** A user-friendly **Streamlit** interface featuring color-coded gauge charts (`Plotly`), sentiment metrics, and raw data displays.
* **🧠 NLP-Driven Insights:** Utilizes **NLTK VADER** to score unstructured text, categorizing sentiment as *Strong Bullish, Bullish, Neutral, Bearish,* or *Strong Bearish*.
* **☁️ Serverless Architecture:** The backend is wrapped with **Mangum** and containerized with **Docker**, designed for scalable deployment on **AWS Lambda**.

---

## 🛠️ Tech Stack

### **Frontend**
* **Streamlit:** Interactive web UI.
* **Plotly:** Dynamic gauge charts for sentiment visualization.

### **Backend**
* **FastAPI:** High-performance API framework.
* **BeautifulSoup4:** Web scraping for FinViz (US data).
* **Feedparser:** Parsing Google News RSS feeds (Global data).
* **Deep-Translator:** Real-time language translation.
* **NLTK (VADER):** Sentiment analysis engine.
* **Mangum:** ASGI adapter for AWS Lambda.

---

## ⚡ Quick Start (Local Development)

The project consists of two parts: the FastAPI backend and the Streamlit frontend. You need to run both to use the dashboard.

### 1. Prerequisites
* Python 3.11+
* Docker (Optional, for container deployment)

### 2. Installation
Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
