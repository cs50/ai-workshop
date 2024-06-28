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

    chat_completion_stream = client.chat.completions.create(
        messages=messages,
        model="gpt-4",

        temperature=0.2,
        stream=True,
    )

    print(f"Assistant: ", end="", flush=True)

    response_text = ""

    for part in chat_completion_stream:

        delta = part.choices[0].delta.content or ""

        response_text += delta

        print(delta, end="", flush=True)
    else:

        messages.append({"role": "assistant", "content": response_text})

        print()
