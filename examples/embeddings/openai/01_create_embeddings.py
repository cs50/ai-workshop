import json
import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI module to use OpenAI's API
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define a function to get the embedding of a text using a specified model
def get_embedding(text, model="text-embedding-3-small"):

    # Replace newline characters with spaces in the text
    text = text.replace("\n", " ")

    # Use the OpenAI client to create embeddings for the text using the specified model
    # and return the first embedding from the result
    return client.embeddings.create(input=[text], model=model).data[0].embedding


# Open the file 'ai.txt' from the 'data/transcripts' directory in read mode
FILE_PATH = "../../../data/transcripts/ai.txt"
with open(FILE_PATH, "r") as f:

    # Read the entire content of the file into 'data'
    data = f.read()

    # Split the data into chunks of 500 characters and store them in a list called 'chunks'
    chunks = [data[i:i+500] for i in range(0, len(data), 500)]

    # Initialize a dictionary to hold the mapping of text chunks to their embeddings
    embeddings = {}

    # Loop through each chunk in the chunks list
    print("Creating embeddings...")
    for chunk in chunks:

        # Get the embedding for the current chunk and store it in the 'embeddings' dictionary
        embeddings[chunk] = get_embedding(chunk)

    # Open a new file 'embeddings.jsonl' in write mode
    print("Writing embeddings to file...")
    with open("embeddings.jsonl", "w") as f:

        # Loop through the items in the 'embeddings' dictionary
        for chunk, embedding in embeddings.items():

            # Write each chunk and its embedding as a JSON object to the 'embeddings.jsonl' file
            f.write((f'{{"text": {json.dumps(chunk)}, "embedding": {embedding}}}\n'))

    print("Embeddings written to file 'embeddings.jsonl'")
