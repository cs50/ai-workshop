import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library for API interactions
from openai import OpenAI

# Initialize the OpenAI API client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define a system prompt that sets the context for the conversation.
system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Initialize a list to keep track of the conversation messages
messages = []

# Add the system prompt to the messages list with the role 'system' to set the context for the chat
messages.append({"role": "system", "content": system_prompt})

# Start an infinite loop to continually accept user input and generate responses
while True:

    # Prompt the user for input
    user_prompt = input("User: ")

    # Append the user's message to the conversation with the role 'user'
    messages.append({"role": "user", "content": user_prompt})

    # Request a chat completion from the OpenAI API based on the conversation so far
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",  # Specifies using the "gpt-4o" model
    )

    # Extract the response text from the completion
    response_text = chat_completion.choices[0].message.content

    # Print the assistant's response, stripping any leading/trailing whitespace
    print(f"Assistant: {response_text.strip()}")

    # Append the assistant's response to the conversation, allowing the AI to maintain context in future interactions
    messages.append({"role": "assistant", "content": response_text})
