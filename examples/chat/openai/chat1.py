import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI

# Create a client instance to interact with the OpenAI API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Prompt the user for input and store the input in a variable
user_prompt = input("User: ")

# Use the client to create a chat completion. This involves sending the user's input to the model and receiving a response.
# The `messages` parameter is a list of messages, with each message being a dictionary specifying the role (e.g., "user") and the content of the message.
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": user_prompt}  # The message sent to the model is the user's input
    ],
    model="gpt-4o",  # Specifies that we are using the "gpt-4o" model for this completion
)

# Extract the response text from the first choice of the chat completion. The API can return multiple choices, but here we are only interested in the first one.
response_text = chat_completion.choices[0].message.content

# Print the response from the assistant, formatted with a prefix to indicate that it's the assistant's message.
print(f"Assistant: {response_text}")
