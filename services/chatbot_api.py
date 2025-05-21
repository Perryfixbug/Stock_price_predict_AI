from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "distilgpt2"  # Nhẹ và chạy ổn định trên CPU

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Đảm bảo có pad_token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def generate_reply(prompt: str, history: str = "") -> str:
    """
    Chatbot tài chính đơn giản dùng distilgpt2
    """
    full_prompt = (
        "Q: What is the best way to invest money?\n"
        "A: Diversify your investments across different asset classes like stocks, bonds, and real estate to minimize risk.\n\n"
        "Q: How does the stock market work?\n"
        "A: The stock market is where investors buy and sell shares of public companies. Prices are determined by supply and demand.\n\n"
        f"Q: {prompt}\nA:"
    )

    inputs = tokenizer.encode(full_prompt, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_new_tokens=150,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = decoded.split(f"Q: {prompt}\nA:")[-1].strip()
    return answer

