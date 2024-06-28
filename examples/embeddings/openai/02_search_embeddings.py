from openai import OpenAI
import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embedding(text, model="text-embedding-3-small"):

    text = text.replace("\n", " ")

    return client.embeddings.create(input=[text], model=model).data[0].embedding


with open('embeddings.jsonl', 'r') as f:

    lines = f.readlines()

    embeddings = {}

    for line in lines:

        line = json.loads(line)

        embeddings[line['text']] = line['embedding']


query = input("Enter a query: ")


query_embedding = get_embedding(query)


best_chunk = None
best_score = float("-inf")


for chunk, embedding in embeddings.items():

    score = np.dot(embedding, query_embedding)

    if score > best_score:
        best_chunk = chunk
        best_score = score


print(best_chunk)
