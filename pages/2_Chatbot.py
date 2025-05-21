import streamlit as st
from services.chatbot_api import generate_reply

st.set_page_config(page_title="InvestAI - Chatbot", layout="wide")
st.title("🤖 InvestAI - Trợ lý đầu tư tài chính")

# Khởi tạo lịch sử chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị hội thoại
for msg in st.session_state.chat_history:
    align = "left" if msg["role"] == "ai" else "right"
    color = "#28a745" if msg["role"] == "ai" else "#333"
    st.markdown(
        f"""
        <div style='text-align:{align}; margin-bottom:10px;'>
            <span style='display:inline-block; background-color:{color}; color:white; padding:10px 15px; border-radius:15px; max-width:70%;'>
                {msg['text']}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Form nhập liệu
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("Aa", label_visibility="collapsed", placeholder="Nhập câu hỏi...")
    submitted = st.form_submit_button("Gửi")

# Xử lý câu hỏi người dùng
if submitted and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "ai", "text": "🤖 Đang suy nghĩ..."})
    st.session_state.generating = True  # <-- cờ trạng thái
    st.rerun()

if st.session_state.get("generating", False):
    # Ghép hội thoại và tạo phản hồi
    history_text = "\n".join(
        [f"User: {msg['text']}" if msg["role"] == "user" else f"Assistant: {msg['text']}"
         for msg in st.session_state.chat_history[:-1]]
    )
    last_user_input = [msg["text"] for msg in reversed(st.session_state.chat_history) if msg["role"] == "user"][0]
    ai_response = generate_reply(last_user_input, history_text)

    st.session_state.chat_history[-1]["text"] = ai_response
    st.session_state.generating = False
    st.rerun()