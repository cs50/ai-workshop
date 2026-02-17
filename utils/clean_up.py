# This script deletes all files and vector stores from your OpenAI account.
# !!! Proceed with caution, as this action is irreversible. !!!

import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Prompt user to confirm deletion
confirmation = input("Are you sure you want to delete all files and vector stores? (yes/no) ")
if confirmation != "yes":
    print("Exiting...")
    exit()

# Delete all files
all_files = client.files.list()
for file in all_files:
    try:
        response = client.files.delete(file.id)
        print(response)
    except Exception as e:
        print(e)

# Delete all vector stores
all_vector_stores = client.vector_stores.list()
for vector_store in all_vector_stores:
    try:
        response = client.vector_stores.delete(vector_store.id)
        print(response)
    except Exception as e:
        print(e)
