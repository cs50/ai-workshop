# Import the OpenAI library, which allows us to interact with OpenAI's API
from openai import OpenAI

# Create a client instance to interact with the OpenAI API
client = OpenAI()

# Use the client to create a chat completion. This involves sending a message to the model and receiving a response.
# The `messages` parameter is a list of messages where each message is a dictionary specifying the role (e.g., "user") and the content of the message.
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello, World!"}  # The message sent to the model: a user saying "Hello, World!"
    ],
    model="gpt-4"  # Specifies that we are using the "gpt-4" model for this completion
)

# Extract the response text from the first choice of the chat completion. The API can return multiple choices, but here we are only interested in the first one.
response_text = chat_completion.choices[0].message.content

# Print the response from the assistant, formatted with a prefix to indicate that it's the assistant's message.
print(f"Assistant: {response_text}")
