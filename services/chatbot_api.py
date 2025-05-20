# generate.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Thay model_name nếu muốn mô hình nhẹ hơn
MODEL_NAME = "distilgpt2"   

# Tải tokenizer và mô hình một lần
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",               # Tự chọn GPU hoặc CPU
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    low_cpu_mem_usage=True
)

def generate_reply(prompt: str, history: str = "") -> str:
    """
    Sinh phản hồi từ mô hình dựa trên prompt và lịch sử hội thoại.
    """
    full_prompt = history + f"User: {prompt}\nAssistant:"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id, 
        eos_token_id=tokenizer.eos_token_id
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("Assistant:")[-1].strip()
