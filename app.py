import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from services.stock_api import get_info_data, get_historical_data
from models.full_code import RandomForestRegressor, RegressionTreeNode, best_split, mse
import requests
import pickle
import config
from services.chatbot_api import ask_openai
import openai

st.set_page_config(
    page_title="InvestAI",
    layout="wide",
    initial_sidebar_state="expanded",
)


#App Page
st.header("InvestAI")
col_left, col_right = st.columns([2, 1])

#Left side
with col_left:
    # -- Search bar
    with st.container():
        st.subheader("Tìm kiếm")
        col1, col2 = st.columns([5, 1])
        with col1:
            search_input = st.text_input(
                label="",
                value="AAPL",
                placeholder="Tìm kiếm: AAPL, NVDA,...",
                label_visibility="collapsed"
            )

        with col2:
            search_button = st.button("Tìm kiếm", use_container_width=True)
    # -- Company InfoCompany Info
    info = get_info_data(search_input)
    
    # Kiểm tra xem change có dương hay âm và thay đổi màu sắc
    change_color = "green" if info["change"] > 0 else "red"
    change_sign = "+" if info["change"] > 0 else ""

    # Hiển thị thông tin
    st.markdown(f"### {info['name']} ({info['symbol']})")
    st.markdown(f"**${info['price']}**  :{change_color}[{change_sign}{info['change']}%]  \n*At close: Apr 25, 2025, 4:00 PM*")
    
    # -- Chart
    # 1. Chuẩn bị dữ liệu gốc
    # Lấy dữ liệu
    data_day = get_historical_data(search_input, period='2mo', interval='1d')
    data_week = get_historical_data(search_input, period='15mo', interval='1wk')
    data_month = get_historical_data(search_input, period='5y', interval='1mo')

    # 2. Vẽ Scatter ban đầu (mặc định là 1D)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data_day['Date'],
        y=data_day['Close'],
        mode='lines+markers',
        name='Close',
        line=dict(color='blue'),
        hovertemplate='Giá: %{y}<br>Ngày: %{x}<extra></extra>'
    ))

    # 3. Tạo Buttons để chuyển đổi
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="1D", method="update",
                        args=[{"x": [data_day['Date']], "y": [data_day['Close']],
                                "type": "scatter"},
                            {"title": "Biểu đồ Giá theo Ngày (2 tháng)"}]),

                    dict(label="1W", method="update",
                        args=[{"x": [data_week['Date']], "y": [data_week['Close']],
                                "type": "scatter"},
                            {"title": "Biểu đồ Giá theo Tuần (12 tháng)"}]),

                    dict(label="1M", method="update",
                        args=[{"x": [data_month['Date']], "y": [data_month['Close']],
                                "type": "scatter"},
                            {"title": "Biểu đồ Giá theo Tháng (5 năm)"}]),
                ]),
                direction="right",
                x=0, y=1.15,
                xanchor="left", yanchor="top",
            )
        ],
    )

    # 4. Cài đặt giao diện đẹp
    fig.update_layout(
        title='Biểu đồ Giá chứng khoán',
        template='plotly_dark',
        xaxis_title="Thời gian",
        yaxis_title="Giá",
        xaxis_rangeslider_visible=False
    )

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig)


    # st.plotly_chart(fig, use_container_width=True)
    st.divider()
    # -- News
    #API KEY
    api_key = config.NEWS_API_KEY
    # api_key = "fake"
    
    # URL endpoint
    url = ('https://newsapi.org/v2/everything?'
        'q=stock market&'
        'language=en&'
        'sortBy=publishedAt&'
        f'apiKey={api_key}')

    # Gửi yêu cầu (request)
    response = requests.get(url)

    # Chuyển kết quả JSON thành dict
    data = response.json()
    st.subheader("Tin tức")
    # Lấy 5 bài mới nhất
    news_list = data['articles'][:5]

    for article in news_list:
        st.markdown(f"[{article['title']} - {article['author']}]({article['url']})")

#Right side
with col_right:
    def predict(data, type='day'):
        # Load the model
        with open('models/models.pkl', 'rb') as f:
            models = pickle.load(f)
        
        # Predict using the appropriate model
        return models[type].predict(data)
    
    prediction = {
        "day": round(predict([data_day[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1]], type='day')[0], 2),
        "week": round(predict([data_week[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1]], type='week')[0],2),
        "month": round(predict([data_month[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1]], type='month')[0],2)
    }
    change = {
        "day": round((prediction["day"] - info["price"]) / info["price"] * 100, 2),
        "week": round((prediction["week"] - info["price"]) / info["price"] * 100, 2),
        "month": round((prediction["month"] - info["price"]) / info["price"] * 100, 2)
    }
    change_color = {
        "day": "red" if change["day"] < 0 else "green",
        "week": "red" if change["week"] < 0 else "green",
        "month": "red" if change["month"] < 0 else "green"
    }

    change_sign = {
        "day": "+" if change["day"] > 0 else "",
        "week": "+" if change["week"] > 0 else "",
        "month": "+" if change["month"] > 0 else ""
    }
    
    with st.container():    
        st.subheader("Dự đoán giá")
        st.markdown(f"**Ngắn hạn (1 ngày)**  \n${prediction["day"]} :{change_color['day']}[{change_sign['day']}{change['day']}%]")
        st.markdown(f"**Trung hạn (1 tuần)**  \n${prediction['week']} :{change_color['week']}[{change_sign['week']}{change['week']}%]")
        st.markdown(f"**Dài hạn (1 tháng)**  \n${prediction['month']} :{change_color['month']}[{change_sign['month']}{change['month']}%]")

    st.divider()
     # -- AI Suggestion
    with st.container():
        st.subheader("InvestAI 🤖")
        
        # Khởi tạo lịch sử chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Hiển thị lịch sử CŨ
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Người dùng nhập tin nhắn
        user_input = st.chat_input("Nhập câu hỏi...")

        if user_input:
            # Hiển thị ngay tin nhắn người dùng
            with st.chat_message("user"):
                st.markdown(user_input)
            # Lưu user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Lấy reply từ model
            reply = ask_openai(user_input)

            # Hiển thị ngay reply
            with st.chat_message("assistant"):
                st.markdown(reply)
            # Lưu assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply})

    