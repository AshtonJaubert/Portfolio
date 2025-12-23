import streamlit as st
import requests
import plotly.graph_objects as go

# Title and Layout
st.set_page_config(page_title="MarketPulse Global", page_icon="🌍")
st.title("🌍 MarketPulse: Global Sentiment Analyzer")
st.markdown("Analyze stock sentiment across international markets (US, Mexico, China/Taiwan).")

# Layout: 2 Columns for Inputs
col_input, col_lang = st.columns([2, 1])

with col_input:
    ticker = st.text_input("Stock Ticker", value="TSLA", help="Enter a US Ticker Symbol").upper()

with col_lang:
    lang_choice = st.selectbox(
        "News Source / Language",
        options=["English (US)", "Spanish (Mexico)", "Mandarin (China/TW)"],
        index=0
    )

# Map UI choice to API code
lang_map = {
    "English (US)": "en",
    "Spanish (Mexico)": "es",
    "Mandarin (China/TW)": "zh"
}
selected_lang_code = lang_map[lang_choice]

if st.button("Analyze Global Sentiment"):
    with st.spinner(f"Fetching {lang_choice} news for {ticker} & translating..."):
        try:
            # Connect to Backend (Using 127.0.0.1 for Mac compatibility)
            api_url = f"http://127.0.0.1:8000/analyze/{ticker}?lang={selected_lang_code}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                data = response.json()
                
                score = data['sentiment_score']
                label = data['sentiment_label']
                count = data['headlines_analyzed']
                
                # Color Logic
                if "Bullish" in label:
                    color = "green"
                elif "Bearish" in label:
                    color = "red"
                else:
                    color = "gray"

                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Ticker", ticker)
                m1.metric("Language Source", selected_lang_code.upper())
                m2.metric("Headlines Scanned", count)
                m3.metric("Global Sentiment", label, delta=score)
                
                # Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': f"Market Sentiment ({lang_choice})"},
                    gauge = {
                        'axis': {'range': [-1, 1]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [-1, -0.05], 'color': "#ffcccb"},
                            {'range': [-0.05, 0.05], 'color': "lightgray"},
                            {'range': [0.05, 1], 'color': "#90ee90"}
                        ],
                        'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': score}
                    }
                ))
                st.plotly_chart(fig)
                
                if selected_lang_code != "en":
                    st.info("ℹ️ Note: Foreign headlines were automatically translated to English for NLP processing.")

            else:
                st.error("Could not find news data. Try a major ticker like TSLA, AAPL, or BABA.")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")