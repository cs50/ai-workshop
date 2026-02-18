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

# Delete all files (re-fetch each page since deletion invalidates cursors)
while True:
    page = client.files.list(limit=100)
    if not page.data:
        break
    for file in page.data:
        try:
            response = client.files.delete(file.id)
            print(response)
        except Exception as e:
            print(e)

# Delete all vector stores (re-fetch each page since deletion invalidates cursors)
while True:
    page = client.vector_stores.list(limit=100)
    if not page.data:
        break
    for vector_store in page.data:
        try:
            response = client.vector_stores.delete(vector_store.id)
            print(response)
        except Exception as e:
            print(e)
