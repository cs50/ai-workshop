import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI

# Create a client instance to interact with the OpenAI API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define the developer prompt which sets the context for the chatbot.
developer_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Initialize a list to keep track of the conversation messages
messages = []

# Add the developer prompt to the messages list with the role 'developer' to set the context for the chat
messages.append({"role": "developer", "content": developer_prompt})

# Start an infinite loop to continually accept user input and generate responses
while True:

    # Prompt the user for input
    user_prompt = input("User: ")

    # Append the user's message to the conversation with the role 'user'
    messages.append({"role": "user", "content": user_prompt})

    # Request a response from the OpenAI API based on the conversation so far
    response = client.responses.create(
        input=messages,
        model="gpt-5",  # Specifies using the "gpt-5" model
    )

    # Extract the response text from the response object.
    response_text = response.output_text

    # Print the response from the assistant, formatted with a prefix to indicate that it's the assistant's message.
    print(f"Assistant: {response_text.strip()}")

    # Append the assistant's response to the conversation, allowing the AI to maintain context in future interactions
    messages.append({"role": "assistant", "content": response_text})
