from services.chatbot_api import generate_reply

# question = "Cường quốc số 1 thế giới"
# response = generate_reply(question)
# print("Chatbot tài chính trả lời:\n", response)

while True:
    user_input = input("Bạn hỏi: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Tạm biệt!")
        break

    response = generate_reply(user_input)
    print("Chatbot tài chính trả lời:\n", response)