import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

system_instruction = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_instruction
    )

convo = model.start_chat()

while True:

    user_input = input("User: ")
    convo.send_message(user_input)
    print(f"Assistant: {convo.last.text.strip()}")