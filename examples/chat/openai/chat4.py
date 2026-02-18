import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent

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
    response_stream = client.responses.create(
        input=messages,
        model="gpt-5.2",
        stream=True,  # Enable streaming to receive the response incrementally
    )

    # Prepare to print the assistant's response incrementally
    print(f"Assistant: ", end="", flush=True)

    # Initialize a variable to accumulate the response text
    response_text = ""

    # Iterate over each part of the streamed response
    for event in response_stream:
        if isinstance(event, ResponseTextDeltaEvent):

            # Extract the text delta from the current streaming event
            delta = event.delta

            # Accumulate the response text
            response_text += delta

            # Print the current part of the response, without adding a new line
            print(delta, end="", flush=True)
    else:

        # Append the assistant's response to the conversation, allowing the AI to maintain context in future interactions
        messages.append({"role": "assistant", "content": response_text})

        # Print a newline once the entire response has been streamed
        print()
