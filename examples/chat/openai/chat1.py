from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


user_prompt = input("User: ")


chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": user_prompt}
    ],
    model="gpt-4",
)


response_text = chat_completion.choices[0].message.content


print(f"Assistant: {response_text}")
