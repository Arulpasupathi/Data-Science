import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Finance Analysis", layout="wide")

COMPANIES = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
}

@st.cache_data
def load_ticker_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return info

@st.cache_data
def load_history(ticker_symbol, period="1y", interval="1d"):
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period=period, interval=interval)
    return history

st.title("Finance Analysis")

company_name = st.selectbox("Choose a company", list(COMPANIES.keys()))
ticker_symbol = COMPANIES[company_name]

with st.spinner("Loading data..."):
    info = load_ticker_info(ticker_symbol)
    history = load_history(ticker_symbol)

st.markdown(f"### {company_name} ({ticker_symbol})")

tabs = st.tabs(["Overview", "Price Analysis", "Volume Analysis"])

with tabs[0]:
    st.subheader("Company Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Sector**", info.get("sector", "N/A"))
        st.write("**Industry**", info.get("industry", "N/A"))
        st.write("**Country**", info.get("country", "N/A"))
        st.write("**Market Cap**", info.get("marketCap", "N/A"))
        st.write("**Previous Close**", info.get("previousClose", "N/A"))
    with col2:
        st.write("**52 Week High**", info.get("fiftyTwoWeekHigh", "N/A"))
        st.write("**52 Week Low**", info.get("fiftyTwoWeekLow", "N/A"))
        st.write("**Trailing P/E**", info.get("trailingPE", "N/A"))
        st.write("**Forward P/E**", info.get("forwardPE", "N/A"))
        st.write("**Volume**", info.get("volume", "N/A"))

    st.markdown("#### Key Financial Summary")
    summary = {
        "Market Cap": info.get("marketCap", "N/A"),
        "Enterprise Value": info.get("enterpriseValue", "N/A"),
        "Beta": info.get("beta", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "52 Week Range": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}"
    }
    st.write(summary)

with tabs[1]:
    st.subheader("Price Analysis")
    price_period = st.selectbox("Select period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    price_history = load_history(ticker_symbol, period=price_period)
    price_history = price_history.dropna(subset=["Close"])
    price_history["SMA_20"] = price_history["Close"].rolling(window=20).mean()
    price_history["SMA_50"] = price_history["Close"].rolling(window=50).mean()

    st.line_chart(price_history[["Close", "SMA_20", "SMA_50"]])
    st.write("Latest closing price:", price_history["Close"].iloc[-1])
    st.write("Latest daily change:", f"{price_history['Close'].pct_change().iloc[-1] * 100:.2f}%")

with tabs[2]:
    st.subheader("Volume Analysis")
    volume_period = st.selectbox("Select volume period", ["1mo", "3mo", "6mo", "1y"], index=3)
    volume_history = load_history(ticker_symbol, period=volume_period)
    volume_history = volume_history.dropna(subset=["Volume"])
    volume_history["Volume_MA_20"] = volume_history["Volume"].rolling(window=20).mean()

    st.bar_chart(volume_history["Volume"])
    st.line_chart(volume_history["Volume_MA_20"])
    st.write("Average volume (20 days):", int(volume_history["Volume_MA_20"].iloc[-1]))

