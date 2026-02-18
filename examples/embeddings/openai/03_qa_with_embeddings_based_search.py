import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

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

# Developer prompt that sets the context for the Responses API call
developer_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Prompt the user for their query
user_query = input("User: ")

# Step 1: Embed the user's query
print(f"\n[Step 1] Embedding the query...")
query_embedding = get_embedding(user_query)

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

# Step 2: Display the best matching chunk found via embedding search
print(f"\n[Step 2] Searching for the most relevant chunk...")
print(f"{'='*60}")
print(f"Best match (score: {best_score:.4f})")
print(f"{'='*60}")
print(best_chunk)
print(f"{'='*60}")

# Prepare the prompt for the response by including the best matching chunk and the user's query
prompt = "Answer the question using the following information delimited by triple brackets:\n\n"
prompt += f"```\n{best_chunk}\n```"
prompt += "\nQuestion: " + user_query

# Step 3: Show how the prompt is constructed from the search result and the user's query
print(f"\n[Step 3] Building prompt with search result + user query...")
print(f"{'-'*60}")
print(prompt)
print(f"{'-'*60}\n")

# Step 4: Generate a response using the OpenAI Responses API with the prepared prompt and developer context
print(f"[Step 4] Sending prompt to the model...")
response = client.responses.create(
    input=[
        {"role": "developer", "content": developer_prompt},
        {"role": "user", "content": prompt}
    ],
    model="gpt-5.2",
)

# Extract the response text from the response object
response_text = response.output_text

# Print the assistant's response
print(f"\n{'='*60}")
print(f"Assistant: {response_text}")
print(f"{'='*60}")
