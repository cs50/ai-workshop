import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI

# Create a client instance to interact with the OpenAI API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Use the client to create a response. This involves sending a message to the model and receiving a response.
# The `input` parameter is a list of messages where each message is a dictionary specifying the role (e.g., "user") and the content of the message.
response = client.responses.create(
    input=[
        {"role": "user", "content": "Hello, World!"}  # The message sent to the model: a user saying "Hello, World!"
    ],
    model="gpt-5"  # Specifies that we are using the "gpt-5" model for this response
)

# Extract the response text from the response object.
response_text = response.output_text

# Print the response from the assistant, formatted with a prefix to indicate that it's the assistant's message.
print(f"Assistant: {response_text}")
