import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def clean_up(vector_store_id, file_ids):
    """Delete the vector store and uploaded files."""

    client.beta.vector_stores.delete(vector_store_id)
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
vector_store = client.beta.vector_stores.create(
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

# Use the Responses API with the file_search tool to answer based on uploaded documents
response = client.responses.create(
    model="gpt-5.2",
    instructions=instructions,
    input=user_input,
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store.id]
    }]
)

# Print the response from the assistant
print(f"Assistant: {response.output_text}")

# Clean up the vector store and uploaded files
clean_up(vector_store.id, file_ids)
