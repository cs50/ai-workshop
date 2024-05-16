import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def get_embedding(chunk, model="models/embedding-001"):
    '''
        'embedding input into vector representation'
    args:
        chunk (str): raw input data string
        model (str): gemini embedding model name
    return:
        embbeding (arr): vector representation
    '''
    # Create embedding
    result = genai.embed_content(
        model=model,
        content=chunk,
    )

    return result['embedding']

# Open the 'embeddings.jsonl' file in read mode
with open('embeddings.jsonl', 'r') as f:

    # Read all lines from the file
    lines = f.readlines()

    # Initialize a dictionary to load the embeddings
    embeddings = {}

    # Loop through each line in the file
    for line in lines:

        # Parse the JSON object in the line
        line = json.loads(line)

        # Map the text chunk to its corresponding embedding in the embeddings dictionary
        embeddings[line['text']] = line['embedding']

# Prompt the user to enter a query
query = input("Enter a query: ")

# Get the embedding for the query
query_embedding = get_embedding(query)

# Initialize variables to track the best matching chunk and its score
best_chunk = None
best_score = float("-inf")

# Loop through each chunk and its embedding in the embeddings dictionary
for chunk, embedding in embeddings.items():

    # Compute the similarity score as the dot product of the embedding vectors
    score = np.dot(embedding, query_embedding)

    # If this score is better than the best score found so far,
    # update the best_chunk and best_score with the current chunk and score
    if score > best_score:
        best_chunk = chunk
        best_score = score

    # Note: OpenAI embeddings are normalized to length 1, which means that:
    # Cosine similarity can be computed slightly faster using just a dot product
    # Cosine similarity and Euclidean distance will result in the identical rankings
    # https://help.openai.com/en/articles/6824809-embeddings-frequently-asked-questions

# Print the chunk that is most similar to the query
print(best_chunk)
