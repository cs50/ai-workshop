import os
from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

messages = []

while True:

    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})

    message = client.messages.create(
        system=system_prompt,
        messages=messages,
        model="claude-3-opus-20240229",
        max_tokens=1024
    )

    response_text = message.content[0].text
    print(f"Assistant: {response_text}")

    messages.append({"role": "assistant", "content": response_text})