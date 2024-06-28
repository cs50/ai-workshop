from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embedding(text, model="text-embedding-3-small"):

    text = text.replace("\n", " ")

    return client.embeddings.create(input=[text], model=model).data[0].embedding


FILE_PATH = "../../../data/transcripts/ai.txt"
with open(FILE_PATH, "r") as f:

    data = f.read()

    chunks = [data[i:i+500] for i in range(0, len(data), 500)]

    embeddings = {}

    print("Creating embeddings...")
    for chunk in chunks:

        embeddings[chunk] = get_embedding(chunk)

    print("Writing embeddings to file...")
    with open("embeddings.jsonl", "w") as f:

        for chunk, embedding in embeddings.items():

            f.write(
                (f'{{"text": {json.dumps(chunk)}, "embedding": {embedding}}}\n'))

    print("Embeddings written to file 'embeddings.jsonl'")
