import os
import time
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def clean_up(assistant_id, thread_id, vector_store_id, file_ids):
    """Delete the assistant, thread, vector store, and uploaded files. """

    client.beta.assistants.delete(assistant_id)
    client.beta.threads.delete(thread_id)
    client.beta.vector_stores.delete(vector_store_id)
    [client.files.delete(file_id) for file_id in file_ids]


FILES_DIR = "../../../data/transcripts/"
file_ids = []

# Iterate over each file in the specified directory
for file in sorted(os.listdir(FILES_DIR)):

    # Upload each file to the OpenAI platform with the purpose set to 'assistants'
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

# Create an assistant with the specified instructions, persona, and behavior
instructions = (
    "You are a friendly and supportive teaching assistant for CS50."
    "You are also a rubber duck."
    "Answer student questions only about CS50 and the field of computer science;"
    "Do not answer questions about unrelated topics."
    "Do not provide full answers to problem sets, as this would violate academic honesty"
)
assistant = client.beta.assistants.create(
    instructions=instructions,
    name="CS50 Duck",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    model="gpt-4o",
)
print(f"Created assistant: {assistant.id} - {assistant.name}")

# Create a new thread
thread = client.beta.threads.create()
thread_message = client.beta.threads.messages.create(
    thread.id,
    role="user",
    content=input("User: ")
)

# Create a new run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Continuously check the status of the assistant's processing
print(f"Running assistant: {assistant.id} in thread: {thread.id}")
while True:

    # Retrieve the latest status of the assistant's processing
    _run = client.beta.threads.runs.retrieve(thread_id=run.thread_id, run_id=run.id)
    # print(f"run status: {_run.status}")

    # If processing is complete, display the assistant's response and exit the loop
    if _run.status == "completed":
        thread_messages = client.beta.threads.messages.list(run.thread_id)
        print(f"Assistant: {thread_messages.data[0].content[0].text.value}")

        # Clean up the assistant, thread, vector store, and uploaded files
        clean_up(assistant.id, thread.id, vector_store.id, file_ids)
        break

    # Wait for a short period before checking the status again
    time.sleep(1)
