import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus
import sys
import os
import config

st.set_page_config(page_title="Quant Volatility Desk", layout="wide")

# --- CONNECT TO ALPACA ---
try:
    client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
    account = client.get_account()
    connected = True
except Exception as e:
    st.error(f"Connection Error: {e}")
    connected = False

# --- SIDEBAR ---
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["Live Desk", "Strategy Logic", "System Architecture"])
st.sidebar.info(f"**Status:** {'🟢 Online' if connected else '🔴 Offline'}")

# --- PAGE 1: LIVE DESK ---
if page == "Live Desk":
    st.title("⚡ Institutional Trading Desk")
    
    if connected:
        equity = float(account.equity)
        last_equity = float(account.last_equity)
        pnl = equity - last_equity
        
        # Top Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Net Liquidation", f"${equity:,.2f}", f"{pnl:+.2f} Today")
        c2.metric("Buying Power", f"${float(account.buying_power):,.2f}")
        c3.metric("Active Strategy", "Vol Reversion (Top 75%)")
        
        # Open Positions
        st.subheader("📦 Open Positions")
        positions = client.get_all_positions()
        if positions:
            pos_data = []
            for p in positions:
                pos_data.append({
                    "Symbol": p.symbol,
                    "Side": p.side.upper(),
                    "Qty": p.qty,
                    "Entry Price": f"${float(p.avg_entry_price):.2f}",
                    "Current Price": f"${float(p.current_price):.2f}",
                    "P/L ($)": f"${float(p.unrealized_pl):.2f}",
                    "P/L (%)": f"{float(p.unrealized_plpc):.2%}"
                })
            st.table(pd.DataFrame(pos_data))
        else:
            st.info("ℹ️ No active positions.")

        # Recent Orders
        st.subheader("📜 Recent Orders")
        try:
            req = GetOrdersRequest(status=OrderStatus.ALL, limit=10, nested=True)
            orders = client.get_orders(req)
            if orders:
                order_data = [{
                    "Time": o.created_at.strftime('%Y-%m-%d %H:%M'),
                    "Symbol": o.symbol if o.symbol else "Multi-Leg",
                    "Type": o.type, 
                    "Side": o.side,
                    "Status": o.status
                } for o in orders]
                st.dataframe(pd.DataFrame(order_data), use_container_width=True)
        except: 
            pass

# --- PAGE 2: STRATEGY LOGIC ---
elif page == "Strategy Logic":
    st.title("🧠 Strategy Visualization")
    
    ticker = st.selectbox("Select Asset", config.PORTFOLIO)
    
    if st.button("Run Analysis"):
        with st.spinner('Fetching Data...'):
            try:
                # Use yfinance for visualization (it works in Streamlit)
                df = yf.download(ticker, period="1y", interval="1d", progress=False)
                
                # Handle MultiIndex headers if present
                if isinstance(df.columns, pd.MultiIndex): 
                    df.columns = df.columns.get_level_values(0)
                
                col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
                
                # Calcs
                df['returns'] = df[col].pct_change()
                df['vol'] = df['returns'].rolling(20).std() * np.sqrt(252)
                df['rank'] = df['vol'].rank(pct=True)
                
                curr_rank = df['rank'].iloc[-1]
                curr_vol = df['vol'].iloc[-1]
                
                # Display
                c1, c2 = st.columns(2)
                c1.metric("Current Volatility", f"{curr_vol:.1%}")
                c2.metric("Vol Rank (Percentile)", f"{curr_rank:.1%}")
                
                if curr_rank > 0.75:
                    st.success(f"✅ TRADE SIGNAL: Volatility is in the top 25%!")
                else:
                    st.warning(f"zzz WAIT SIGNAL: Volatility is too low (<75%)")
                
                # Chart
                st.line_chart(df['vol'])
                
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {e}")

# --- PAGE 3: SYSTEM ARCHITECTURE ---
elif page == "System Architecture":
    st.title("⚙️ System Architecture")
    
    st.markdown("### 📡 Data Pipeline")
    st.code("""
    [Alpaca Market Data] 
           ⬇
    [AWS EC2 Server (Python)] 
           ⬇
    [auto_trader.py]  <-- Analyzes Volatility (20-day Lookback)
           ⬇
    [Execution Engine] <-- Sends Multi-Leg Orders (Iron Condors)
           ⬇
    [Alpaca Brokerage]
    """, language="python")
    
    st.markdown("### 🖥️ Component Status")
    c1, c2, c3 = st.columns(3)
    c1.success("Bot Logic: Active")
    c2.success("Data Feed: Alpaca SIP")
    c3.success("Hosting: AWS Cloud")
    
    st.info("The system runs autonomously 24/7 on AWS, checking markets every 15 minutes during trading hours.")
