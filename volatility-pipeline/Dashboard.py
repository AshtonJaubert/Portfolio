import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from alpaca.trading.client import TradingClient
import sys
import os
import config

st.set_page_config(page_title="Quant Volatility Desk", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS  ---
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;}
    h1 {color: #1e3d59;}
</style>
""", unsafe_allow_html=True)

# --- CONNECTIONS ---
try:
    client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
    account = client.get_account()
    connected = True
except:
    connected = False

# --- SIDEBAR ---
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["Live Desk", "Strategy Logic", "System Architecture"])

st.sidebar.divider()
st.sidebar.info(f"**Status:** {'🟢 Online' if connected else '🔴 Offline'}\n\n**Environment:** AWS Lambda / EC2\n\n**Assets:** {len(config.PORTFOLIO)} Tracked")

# ==========================================
# PAGE 1: LIVE DESK
# ==========================================
if page == "Live Desk":
    st.title("⚡ Institutional Trading Desk")
    st.markdown("Real-time monitoring of the **Short-Duration Iron Condor** strategy running on AWS.")
    
    # METRICS
    if connected:
        equity = float(account.equity)
        bp = float(account.buying_power)
        pnl = float(account.equity) - float(account.last_equity)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Net Liquidation", f"${equity:,.2f}", f"{pnl:+.2f} Today")
        c2.metric("Buying Power", f"${bp:,.2f}")
        c3.metric("Active Strategy", "Volatility Reversion (Top 85%)")
        
        # POSITIONS TABLE
        st.subheader("📦 Open Positions")
        positions = client.get_all_positions()
        
        if positions:
            pos_data = [{
                "Ticker": p.symbol, 
                "Qty": p.qty, 
                "Entry": f"${float(p.avg_entry_price):.2f}", 
                "Current": f"${float(p.current_price):.2f}",
                "P/L ($)": f"${float(p.unrealized_pl):.2f}",
                "P/L (%)": f"{float(p.unrealized_plpc)*100:.2f}%"
            } for p in positions]
            st.table(pd.DataFrame(pos_data))
        else:
            st.info("ℹ️ No active positions. The algorithm is scanning for high-volatility setups.")

# ==========================================
# PAGE 2: STRATEGY LOGIC
# ==========================================
elif page == "Strategy Logic":
    st.title("🧠 Strategy Visualization")
    st.markdown("""
    **The Thesis:** Market participants systematically overpay for protection during volatility spikes. 
    We sell this "expensive fear" via **Iron Condors** and buy it back when volatility reverts to the mean.
    """)
    
    ticker = st.selectbox("Select Asset to Visualize", config.PORTFOLIO)
    
    if st.button("Run Analysis"):
        with st.spinner(f"Analyzing {ticker} Volatility Structure..."):
            df = yf.download(ticker, period="1y", interval="1d", progress=False)
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
            
            df['returns'] = df[col].pct_change()
            df['vol'] = df['returns'].rolling(20).std() * np.sqrt(252)
            df['rank'] = df['vol'].rank(pct=True)
            
            # PLOTLY CHART
            fig = go.Figure()
            
            # Price Trace
            fig.add_trace(go.Scatter(x=df.index, y=df[col], name='Price', line=dict(color='gray')))
            
            # Volatility Trace (Secondary Y)
            fig.add_trace(go.Scatter(x=df.index, y=df['rank'], name='Vol Rank', 
                                   line=dict(color='purple', width=1), yaxis='y2'))
            
            # Danger Zones
            fig.add_hrect(y0=0.85, y1=1.0, fillcolor="green", opacity=0.1, layer="below", line_width=0, yref='y2')
            
            fig.update_layout(
                title=f"{ticker} Price vs. Volatility Rank",
                yaxis=dict(title="Price ($)"),
                yaxis2=dict(title="Vol Percentile (0-1)", overlaying='y', side='right'),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            curr_rank = df['rank'].iloc[-1]
            st.metric("Current Volatility Rank", f"{curr_rank:.1%}")
            if curr_rank > 0.85:
                st.success("✅ TRADING ZONE: Volatility is expensive. Algorithm is ACTIVE.")
            else:
                st.warning("zzz WAIT ZONE: Volatility is cheap. Algorithm is IDLE.")

# ==========================================
# PAGE 3: ARCHITECTURE
# ==========================================
elif page == "System Architecture":
    st.title("⚙️ System Architecture")
    st.markdown("This system is designed for **low-latency cloud execution**.")
    
    st.code("""
    [AWS EC2 / Lambda]
        |
        +-- auto_trader.py (Infinite Loop)
        |       |
        |       +--> Checks Volatility (yfinance)
        |       +--> Places Orders (Alpaca API)
        |       +--> Logs to CloudWatch
        |
        +-- Dashboard.py (Streamlit)
                |
                +--> Connects to Alpaca Read-Only
                +--> Displays Live P&L
    """, language="text")
    
    st.subheader("Tech Stack")
    c1, c2, c3 = st.columns(3)
    c1.info("**Python 3.9**\nCore Logic")
    c2.info("**Alpaca API**\nExecution")
    c3.info("**Streamlit**\nVisualization")