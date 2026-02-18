import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent
from utils import clean_up

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


FILES_DIR = "../../../data/transcripts/"
file_ids = []

# Iterate over each file in the specified directory
for file in sorted(os.listdir(FILES_DIR)):

    # Upload each file to the OpenAI platform for use with file search
    with open(FILES_DIR + file, "rb") as f:
        _file = client.files.create(file=f, purpose="assistants")

    # Append the reference to the uploaded file to the list
    file_ids.append(_file.id)
    print(f"Uploaded file: {_file.id} - {file}")

# Create a vector store using the uploaded files
vector_store = client.vector_stores.create(
  name="CS50 Lecture Captions",
  file_ids=file_ids
)
print(f"Created vector store: {vector_store.id} - {vector_store.name}")

# Define the instructions that set the persona and behavior for the response
instructions = (
    "You are a friendly and supportive teaching assistant for CS50. "
    "You are also a rubber duck. "
    "Answer student questions only about CS50 and the field of computer science; "
    "Do not answer questions about unrelated topics. "
    "Do not provide full answers to problem sets, as this would violate academic honesty."
)

# Store the previous response ID to maintain conversation context across turns
previous_response_id = None

# Start an infinite loop to continually accept user input and generate responses
try:
    while True:

        # Prompt the user for input
        user_input = input("User: ")

        # Use the Responses API with the file_search tool and streaming enabled
        response_stream = client.responses.create(
            model="gpt-5.2",
            instructions=instructions,
            input=user_input,
            previous_response_id=previous_response_id,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store.id]
            }],
            stream=True,
        )

        # Print the assistant's response incrementally as it streams
        print(f"Assistant: ", end="", flush=True)

        # Initialize a variable to capture the completed response
        completed_response = None

        # Iterate over each event in the streamed response
        for event in response_stream:
            if isinstance(event, ResponseTextDeltaEvent):

                # Print the current delta of the response, without adding a new line
                print(event.delta, end="", flush=True)

            # Capture the final response object when streaming completes
            if event.type == "response.completed":
                completed_response = event.response

        # Print a newline once the entire response has been streamed
        print()

        # Save the response ID so the next turn continues the conversation
        if completed_response:
            previous_response_id = completed_response.id

except (KeyboardInterrupt, EOFError):
    # Clean up the vector store and uploaded files when the user exits
    clean_up(client, vector_store.id, file_ids)
