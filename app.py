import streamlit as st
import altair as alt
from services.stock_api import get_stock_price, get_historical_data

st.set_page_config(page_title="📈 Stock Watch", layout="centered")

st.title("📊 Live Stock Tracker")
ticker = st.text_input("Nhập mã cổ phiếu (ví dụ: AAPL, MSFT, VNM):", value="AAPL")

# Chọn khoảng thời gian
period_option = st.selectbox(
    "Chọn khoảng thời gian để xem biểu đồ:",
    options={
        "1d": "1 ngày",
        "1wk": "1 tuần",
        "1mo": "1 tháng",
    },
    format_func=lambda x: {
        "1d": "1 ngày",
        "1wk": "1 tuần",
        "1mo": "1 tháng",
    }[x]
)

# Lấy dữ liệu
if ticker:
    st.subheader(f"📉 Biểu đồ giá cổ phiếu {ticker}")
    historical_data = get_historical_data(ticker, period=period_option)
    if historical_data is not None and not historical_data.empty:
        chart = alt.Chart(historical_data).mark_line().encode(
            x='Date:T',
            y='Close:Q',
            tooltip=['Date:T', 'Close:Q']
        ).properties(
            width=700,
            height=400
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Không có dữ liệu lịch sử.")
