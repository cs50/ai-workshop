import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define a function to get the embedding of a given text using a specified model
def get_embedding(text, model="text-embedding-3-small"):

    # Replace newline characters with spaces to ensure consistent formatting
    text = text.replace("\n", " ")

    # Request the embedding for the text from the OpenAI API and return the first embedding from the result
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Open the 'embeddings.jsonl' file in read mode to load pre-computed embeddings
with open('embeddings.jsonl', 'r') as f:

    # Read all lines from the file
    lines = f.readlines()

    # Initialize a dictionary to store the embeddings
    embeddings = {}

    # Loop through each line in the file, assuming each line is a JSON object
    for line in lines:

        # Parse the JSON object from the line
        line = json.loads(line)

        # Store the text chunk and its corresponding embedding in the dictionary
        embeddings[line['text']] = line['embedding']

# Developer prompt that sets the context for the Responses API call
developer_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Prompt the user for their query
user_query = input("User: ")

# Get the embedding for the user's query using the function defined earlier
query_embedding = get_embedding(user_query)

# Initialize variables to track the best matching chunk and its similarity score
best_chunk = None
best_score = float("-inf")

# Loop through each chunk and its embedding in the embeddings dictionary
for chunk, embedding in embeddings.items():

    # Compute the similarity score as the dot product of the query embedding and the chunk's embedding
    score = np.dot(embedding, query_embedding)

    # Update the best_chunk and best_score if the current score is higher
    if score > best_score:
        best_chunk = chunk
        best_score = score

# Prepare the prompt for the response by including the best matching chunk and the user's query
prompt = "Answer the question using the following information delimited by triple brackets:\n\n"
prompt += f"```\n{best_chunk}\n```"
prompt += "\nQuestion: " + user_query

print(f"Prompt:\n\n{prompt}\n")

# Generate a response using the OpenAI Responses API with the prepared prompt and developer context
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
print(f"Assistant: {response_text}")
