import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def clean_up(vector_store_id, file_ids):
    """Delete the vector store and uploaded files."""

    client.vector_stores.delete(vector_store_id)
    [client.files.delete(file_id) for file_id in file_ids]


FILES_DIR = "../../../data/transcripts/"
file_ids = []

# Iterate over each file in the specified directory
for file in sorted(os.listdir(FILES_DIR)):

    # Upload each file to the OpenAI platform for use with file search
    _file = client.files.create(file=open(FILES_DIR + file, "rb"), purpose="assistants")

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

# Prompt the user for input
user_input = input("User: ")

# Use the Responses API with the file_search tool and streaming enabled
response_stream = client.responses.create(
    model="gpt-5.2",
    instructions=instructions,
    input=user_input,
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store.id]
    }],
    stream=True,
)

# Print the assistant's response incrementally as it streams
print(f"\nAssistant: ", end="", flush=True)

# Iterate over each event in the streamed response
for event in response_stream:
    if isinstance(event, ResponseTextDeltaEvent):

        # Print the current delta of the response, without adding a new line
        print(event.delta, end="", flush=True)

# Print a newline once the entire response has been streamed
print()

# Clean up the vector store and uploaded files
clean_up(vector_store.id, file_ids)
