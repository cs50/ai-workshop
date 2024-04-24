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

    print(f"Assistant: ", end="", flush=True)

    response_text = ""
    with client.messages.stream(
        system=system_prompt,
        messages=messages,
        model="claude-3-opus-20240229",
        max_tokens=1024
    ) as stream:
          for text in stream.text_stream:
            response_text += text
            print(text, end="", flush=True)
          else:
            messages.append({"role": "assistant", "content": response_text})
            print("", flush=True)