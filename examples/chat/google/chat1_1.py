import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

user_input = input("User: ")

generated_content = model.generate_content(
    {"role": "user", "parts": [user_input]}
)
response_text = generated_content.candidates[0].content.parts[0].text.strip()

print(f"Assistant: {response_text}")