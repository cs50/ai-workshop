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

messages = []

while True:

    user_input = input("User: ")
    messages.append({
        "role": "user", "parts": [user_input]
    })

    print(f"Assistant: ", end="", flush=True)
    response_text = ""

    generated_content = model.generate_content(contents=messages, stream=True)

    for each in generated_content:

        delta = each.candidates[0].content.parts[0].text.strip()
        print(delta, end="", flush=True)

        response_text += delta
    else:
        print()

    messages.append({"role": "model", "parts": [response_text]})