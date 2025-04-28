from openai import OpenAI, RateLimitError
import config

# Hàm gửi câu hỏi
def ask_openai(question):
    client = OpenAI(api_key=config.OPENAI_API_KEY_2)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=150,
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        print("Rate limit exceeded or insufficient quota. Please check your OpenAI account.")
        return "Limit API exceeded. Please try again later."
