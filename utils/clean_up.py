# This script deletes all assistants, files, and vector stores from your OpenAI account.
# !!! Proceed with caution, as this action is irreversible. !!!

import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Prompt user to confirm deletion
confirmation = input("Are you sure you want to delete all assistants, files, and vector stores? (yes/no) ")
if confirmation != "yes":
    print("Exiting...")
    exit()

# Delete all assistants
all_assistants = client.beta.assistants.list(order="desc", limit="100",)
for assistant in all_assistants:
    try:
        response = client.beta.assistants.delete(assistant.id)
        print(response)
    except Exception as e:
        print(e)

# Delete all files
all_files = client.files.list()
for file in all_files:
    try:
        response = client.files.delete(file.id)
        print(response)
    except Exception as e:
        print(e)

# Delete all vector stores
all_vector_stores = client.beta.vector_stores.list()
for vector_store in all_vector_stores:
    try:
        response = client.beta.vector_stores.delete(vector_store.id)
        print(response)
    except Exception as e:
        print(e)