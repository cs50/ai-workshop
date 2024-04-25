import os
from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

user_input = input("User: ")

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {"role": "user", "content": user_input}
    ],
    model="claude-3-opus-20240229"
)

response_text = message.content[0].text

print(f"Assistant: {response_text}")
