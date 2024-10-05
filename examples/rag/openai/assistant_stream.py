import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override  # Import override decorator if needed
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define the EventHandler class as per the API documentation
# https://platform.openai.com/docs/assistants/overview?context=with-streaming
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nAssistant: ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        # print(f"\nassistant > {tool_call.type}\n", flush=True)
        pass

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


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

print(f"Running assistant: {assistant.id} in thread: {thread.id}")
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler()
) as stream:
    stream.until_done()
    print()
    clean_up(assistant.id, thread.id, vector_store.id, file_ids)