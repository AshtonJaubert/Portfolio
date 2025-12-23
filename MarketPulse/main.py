import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from bs4 import BeautifulSoup
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import feedparser
from deep_translator import GoogleTranslator

# Initialize FastAPI
app = FastAPI(title="MarketPulse Sentiment API", version="2.0")

# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

class SentimentResponse(BaseModel):
    ticker: str
    sentiment_score: float
    sentiment_label: str
    headlines_analyzed: int
    language: str

def fetch_finviz_news(ticker: str):
    """Scrapes FinViz for English news (Best for US Stocks)"""
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    news_table = soup.find(id='news-table')
    if not news_table:
        return []
        
    headlines = []
    rows = news_table.findAll('tr')
    for row in rows[:30]: # Get top 30
        link = row.find('a')
        if link:
            headlines.append(link.text)
    return headlines

def fetch_google_news(ticker: str, lang: str):
    """Fetches Google News RSS in specific languages"""
    # URL configurations for different regions
    if lang == "es":
        # Spanish (Mexico focus)
        rss_url = f"https://news.google.com/rss/search?q={ticker}&hl=es-419&gl=MX&ceid=MX:es-419"
    elif lang == "zh":
        # Mandarin (Taiwan/Hong Kong focus for better access)
        rss_url = f"https://news.google.com/rss/search?q={ticker}&hl=zh-TW&gl=TW&ceid=TW:zh-TW"
    else:
        return []

    feed = feedparser.parse(rss_url)
    headlines = [entry.title for entry in feed.entries[:20]]
    
    # Translate to English for VADER analysis
    translated_headlines = []
    translator = GoogleTranslator(source='auto', target='en')
    
    for h in headlines:
        try:
            # Simple cleaning to remove source name often found in Google News titles
            clean_h = h.split(" - ")[0] 
            trans = translator.translate(clean_h)
            translated_headlines.append(trans)
        except:
            continue
            
    return translated_headlines

@app.get("/analyze/{ticker}", response_model=SentimentResponse)
def analyze_stock(ticker: str, lang: str = "en"):
    ticker = ticker.upper()
    headlines = []

    try:
        # 1. Select Data Source based on Language
        if lang == "en":
            headlines = fetch_finviz_news(ticker)
        elif lang in ["es", "zh"]:
            headlines = fetch_google_news(ticker, lang)
        
        if not headlines:
            raise HTTPException(status_code=404, detail=f"No news found for {ticker} in language '{lang}'")

        # 2. Analyze Sentiment (VADER works best on English, so we used translation above)
        total_score = 0
        for h in headlines:
            score = analyzer.polarity_scores(h)['compound']
            total_score += score
            
        avg_score = total_score / len(headlines)

        # 3. Determine Label
        if avg_score > 0.15:
            label = "Strong Bullish"
        elif avg_score > 0.05:
            label = "Bullish"
        elif avg_score < -0.15:
            label = "Strong Bearish"
        elif avg_score < -0.05:
            label = "Bearish"
        else:
            label = "Neutral"

        return {
            "ticker": ticker,
            "sentiment_score": round(avg_score, 4),
            "sentiment_label": label,
            "headlines_analyzed": len(headlines),
            "language": lang
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# AWS Lambda Handler
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
