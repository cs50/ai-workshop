from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."


messages = []


messages.append({"role": "system", "content": system_prompt})


while True:

    user_prompt = input("User: ")

    messages.append({"role": "user", "content": user_prompt})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4",
    )

    response_text = chat_completion.choices[0].message.content

    print(f"Assistant: {response_text.strip()}")

    messages.append({"role": "assistant", "content": response_text})
