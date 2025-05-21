import streamlit as st
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import config

ALPHA_VANTAGE_API_KEY = config.ALPHA_VANTAGE_API_KEY_2 

@st.cache_data(ttl=600)
def get_info_data(ticker_symbol: str = "AAPL"):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='json')
    
    # Lấy dữ liệu giá hiện tại
    quote, _ = ts.get_quote_endpoint(symbol=ticker_symbol)
    
    try:
        price = float(quote["05. price"])
        prev_close = float(quote["08. previous close"])
        change_percent = ((price - prev_close) / prev_close) * 100 if prev_close > 0 else 0
    except:
        price, prev_close, change_percent = 0, 0, 0

    return {
        "name": ticker_symbol,  # Alpha Vantage không cung cấp tên dài
        "symbol": ticker_symbol,
        "price": round(price, 2),
        "change": round(change_percent, 2),
        "market_cap": 0,  # Không có trong Alpha Vantage free
        "pe_ratio": 0,     # Không có trong Alpha Vantage free
        "dividend_yield": 0,  # Không có trong Alpha Vantage free
        "time": quote.get("07. latest trading day", "N/A")
    }

@st.cache_data(ttl=600)
def get_all_historical_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

    def fetch(fn):
        time.sleep(1)  # tránh giới hạn rate
        df, _ = fn(symbol=symbol)
        df = df.sort_index().reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        return df

    return {
        "day": fetch(ts.get_daily),       # Dữ liệu hàng ngày (2 tháng gần nhất tương đương)
        "week": fetch(ts.get_weekly),     # Dữ liệu hàng tuần
        "month": fetch(ts.get_monthly)    # Dữ liệu hàng tháng
    }
