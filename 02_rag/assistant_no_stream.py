import os
import time
from openai import OpenAI

# Initialize the OpenAI API client
client = OpenAI()

# Define instructions for the assistant, outlining its persona and behavior
instructions = (
    "You are a knowledgeable and approachable assistant for attendees of SIGCSE 2024. "
    "Engage with inquiries in a friendly manner, offering insights and resources that enhance "
    "the attendees' conference experience. Avoid discussions unrelated to SIGCSE 2024 or the "
    "broader field of computer science education."
)

# Specify the path to the directory containing the data files to be uploaded
file_path = "./data/"

# Initialize a list to hold references to the uploaded files
files = []

# Iterate over each file in the specified directory
for file in os.listdir(file_path):

    # Upload each file to the OpenAI platform with the purpose set to 'assistants'
    file = client.files.create(
        file=open(file_path + file, "rb"), purpose="assistants")
    
    # Append the reference to the uploaded file to the list
    files.append(file)

# Construct a unique identifier for the assistant (for workshop purposes, the assistant name includes the user's GitHub username)
current_assistant = f"sigcse24-workshop105-{os.getenv('GITHUB_USER')}"

# Retrieve a list of all existing assistants and map their names to their IDs
all_assistants = {assistant.name: assistant.id for assistant in client.beta.assistants.list(limit=100).data}

# Check if the assistant with the desired name already exists
if current_assistant not in all_assistants:

    # If not, create a new assistant with the specified name, instructions, tools, and associated files
    assistant = client.beta.assistants.create(
        name=current_assistant,
        instructions=instructions, # specify the assistant's persona and behavior
        tools=[{"type": "retrieval"}], # specify the assistant's capabilities
        file_ids=[file.id for file in files], # all the files uploaded will be associated with the assistant
        model="gpt-4-turbo-preview", # https://platform.openai.com/docs/assistants/overview?context=with-streaming
    )
else:

    # If the assistant already exists, retrieve and use it
    assistant = client.beta.assistants.retrieve(all_assistants[current_assistant])

# Prompt the user for their query
user_prompt = input("User: ")

# Create a new conversation thread with the user's initial query
thread = client.beta.threads.create(
    messages=[{"role": "user", "content": user_prompt}])

# Initiate the assistant's processing on the created thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Continuously check the status of the assistant's processing
print("Awaiting response ...")
while True:

    # Retrieve the latest status of the assistant's processing
    _run = client.beta.threads.runs.retrieve(thread_id=run.thread_id, run_id=run.id)
    # print(f"run status: {_run.status}")

    # If processing is complete, display the assistant's response and exit the loop
    if _run.status == "completed":
        thread_messages = client.beta.threads.messages.list(run.thread_id)
        print(f"Assistant: {thread_messages.data[0].content[0].text.value}")
        break

    # Wait for a short period before checking the status again
    time.sleep(1)
