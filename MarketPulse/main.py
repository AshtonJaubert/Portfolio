import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from bs4 import BeautifulSoup
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Initialize FastAPI
app = FastAPI(title="MarketPulse Sentiment API", version="1.0")

# Download VADER lexicon (Run once on startup)
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

class SentimentResponse(BaseModel):
    ticker: str
    sentiment_score: float
    sentiment_label: str
    headlines_analyzed: int

@app.get("/")
def home():
    return {"message": "MarketPulse API is running. Use /analyze/{ticker} to get sentiment."}

@app.get("/analyze/{ticker}", response_model=SentimentResponse)
def analyze_stock(ticker: str):
    ticker = ticker.upper()
    finviz_url = f"https://finviz.com/quote.ashx?t={ticker}"
    
    try:
        # 1. Fetch Data from FinViz
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(finviz_url, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Ticker not found or FinViz blocked the request.")

        # 2. Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        news_table = soup.find(id='news-table')
        
        if not news_table:
            raise HTTPException(status_code=404, detail="No news table found for this ticker.")

        # 3. Extract Headlines
        headlines = []
        rows = news_table.findAll('tr')
        
        # Get the latest 30 headlines to keep it fast
        for row in rows[:30]:
            # FinViz news rows usually have an <a> tag with the headline
            link_tag = row.find('a')
            if link_tag:
                headlines.append(link_tag.text)

        if not headlines:
             raise HTTPException(status_code=404, detail="No headlines found.")

        # 4. Analyze Sentiment
        total_score = 0
        
        for headline in headlines:
            score = analyzer.polarity_scores(headline)['compound']
            total_score += score
            
        avg_score = total_score / len(headlines)

       # 5. Determine Label
        if avg_score > 0.15:
            label = "Strong Bullish"  # High conviction
        elif avg_score > 0.05:
            label = "Bullish"         # Slight positive tilt
        elif avg_score < -0.15:
            label = "Strong Bearish"  # High conviction
        elif avg_score < -0.05:
            label = "Bearish"         # Slight negative tilt
        else:
            label = "Neutral"         # No strong sentiment

        return {
            "ticker": ticker,
            "sentiment_score": round(avg_score, 4),
            "sentiment_label": label,
            "headlines_analyzed": len(headlines)
        }

    except Exception as e:
        # Print error to console for debugging
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)