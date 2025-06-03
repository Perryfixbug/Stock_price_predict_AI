from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import streamlit as st

# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # Nhẹ và chạy ổn định trên CPU

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     torch_dtype=torch.float16,
#     device_map="auto",
#     token=True
# )

# tokenizer = AutoTokenizer.from_pretrained(
#     MODEL_NAME,
#     token=True
# )

# # Đảm bảo có pad_token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

@st.cache_resource(show_spinner="🤖 Đang tải mô hình AI tài chính...")
def load_model():
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",
        torch_dtype=torch.float16,
        device_map="auto",
        use_auth_token=True  # hoặc dùng token="your_token"
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",
        use_auth_token=True
    )
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    return model, tokenizer

model, tokenizer = load_model()  # chỉ gọi một lần khi lần đầu load app

def generate_reply(prompt: str) -> str:
    """
    Chatbot tài chính dùng Mistral-7B-Instruct
    """

    # Mô tả vai trò và yêu cầu trả lời
    instruction = (
        "You are a helpful and knowledgeable financial assistant. "
        "Answer the question clearly and concisely."
    )

    # Định dạng prompt chuẩn cho Mistral-7B-Instruct
    full_prompt = f"<s>[INST] {instruction}\n\n{prompt} [/INST]"

    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=70,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        # early_stopping=True
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Tách phần sau [/INST]
    if '[/INST]' in decoded:
        answer = decoded.split('[/INST]')[-1].strip()
    else:
        answer = decoded.strip()

    return answer

