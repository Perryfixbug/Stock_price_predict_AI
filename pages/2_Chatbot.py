import streamlit as st
st.set_page_config(page_title="InvestAI - Chatbot", layout="wide")

from services.chatbot_api import generate_reply

col1, col2, col3 = st.columns([1,4,1])
with col2:
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
        col1, col2 = st.columns([8,2])  # chia cột, cột giữa nhỏ để nút
        with col1:
            user_input = st.text_input("Aa", label_visibility="collapsed", placeholder="Nhập câu hỏi...")
        with col2:
            submitted = st.form_submit_button("Gửi", use_container_width=True)  # cho nút full width trong cột nhỏ

    # Xử lý câu hỏi người dùng
    if submitted and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "ai", "text": "🤖 Đang suy nghĩ..."})
        st.session_state.generating = True  # <-- cờ trạng thái
        st.rerun()

    if st.session_state.get("generating", False):
        # Nối toàn bộ lịch sử hội thoại, định dạng "User: xxx" / "Assistant: xxx"
        # history_text = "\n".join(
        #     f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['text']}"
        #     for msg in st.session_state.chat_history[:-1]
        # )

        # Lấy câu hỏi cuối của user
        last_user_input = next(
            (msg["text"] for msg in reversed(st.session_state.chat_history) if msg["role"] == "user"),
            ""
        )
        # Tạo prompt truyền vào generate_reply
        # prompt = history_text + "\nUser: " + last_user_input
        prompt = last_user_input

        # Gọi hàm generate_reply với 1 prompt duy nhất
        # ✅ Hiện spinner khi đang xử lý câu trả lời
        with st.spinner("🤖 Đang phân tích và trả lời..."):
            ai_response = generate_reply(prompt)

        # Cập nhật câu trả lời vào chat_history
        st.session_state.chat_history[-1]["text"] = ai_response
        st.session_state.generating = False
        st.rerun()