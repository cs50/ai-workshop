import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI

# Create a client instance to interact with the OpenAI API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Prompt the user for input and store the input in a variable
user_prompt = input("User: ")

# Define the developer prompt which sets the context for the chatbot.
developer_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Use the client to create a response by sending a message and receiving a reply.
# The `input` parameter is a list of messages, each a dictionary with a role (e.g., "user") and content.
# Developer messages provide context, and user messages contain the prompt.
response = client.responses.create(
    input=[
        {"role": "developer", "content": developer_prompt},  # The developer/context message
        {"role": "user", "content": user_prompt}  # The user's message
    ],
    model="gpt-5",  # Specifies using the "gpt-5" model for generating responses
)

# Extract the response text from the response object.
response_text = response.output_text

# Print the response from the assistant, formatted with a prefix to indicate that it's the assistant's message.
print(f"Assistant: {response_text}")
