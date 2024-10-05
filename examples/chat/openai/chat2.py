import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to enable API interactions
from openai import OpenAI

# Initialize the OpenAI API client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define the system prompt which sets the context for the chatbot.
system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Prompt the user for input and store the response in a variable
user_prompt = input("User: ")

# Send the system and user prompts to the OpenAI API, requesting a chat completion. The 'system' role sets the context, and the 'user' role represents the user's input.
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},  # The system/context message
        {"role": "user", "content": user_prompt}  # The user's message
    ],
    model="gpt-4o",  # Specifies using the "gpt-4o" model for generating responses
)

# Extract the chatbot's response from the completion
response_text = chat_completion.choices[0].message.content

# Display the chatbot's (assistant's) response
print(f"Assistant: {response_text}")
