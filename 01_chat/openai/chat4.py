# Import the OpenAI library for API interactions
from openai import OpenAI

# Initialize the OpenAI API client
client = OpenAI()

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
    chat_completion_stream = client.chat.completions.create(
        messages=messages,
        model="gpt-4",
        # Sets the sampling temperature to control randomness (0 makes output deterministic, 1 maximizes randomness, with 0.2 being more focused and less random).
        temperature=0.2,
        stream=True,  # Enable streaming for long-running completions
    )

    # Prepare to print the assistant's response incrementally
    print(f"Assistant: ", end="", flush=True)

    # Initialize a variable to accumulate the response text
    response_text = ""

    # Iterate over each part of the streamed response
    for part in chat_completion_stream:

        # Extract text content from the current part; fallback to an empty string if none
        delta = part.choices[0].delta.content or ""

        # Accumulate the response text
        response_text += delta

        # Print the current part of the response, without adding a new line
        print(delta, end="", flush=True)
    else:
        # Print a newline once the entire response has been streamed
        print()

    # Append the assistant's response to the conversation, allowing the AI to maintain context in future interactions
    messages.append({"role": "assistant", "content": response_text})
