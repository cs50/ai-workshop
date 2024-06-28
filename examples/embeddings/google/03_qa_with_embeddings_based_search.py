import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ============ Prompt query + add system prompt===========================

# System prompt that sets the context for the chat completion API call
system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."

# Prompt the user for their query
user_query = input("User: ")

# ================ Search embeddings (Retrieve) =====================================
# Get the embedding for the user's query using the function defined earlier
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

def load_embeddings():
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

        return embeddings


query_embedding = get_embedding(user_query)

# Initialize variables to track the best matching chunk and its similarity score
best_chunk = None
best_score = float("-inf")

# Loop through each chunk and its embedding in the embeddings dictionary
embeddings = load_embeddings()
for chunk, embedding in embeddings.items():

    # Compute the similarity score as the dot product of the query embedding and the chunk's embedding
    score = np.dot(embedding, query_embedding)

    # Update the best_chunk and best_score if the current score is higher
    if score > best_score:
        best_chunk = chunk
        best_score = score

# ========= Augment prompt===========================================================================
# Prepare the prompt for the chat completion by including the best matching chunk and the user's query
prompt = "Answer the question using the following information delimited by triple brackets:\n\n"
prompt += f"```\n{best_chunk}\n```"
prompt += "\nQuestion: " + user_query
prompt += "\nDon't say based on information provided or something like that"


# ========================= Response ================================================
# Generate a response using the Gemini API with the prepared prompt and system context
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_prompt
)

messages = [
    {'role':'user', 'parts': [prompt]},
]
generated_content = model.generate_content(messages)
response_text = generated_content.candidates[0].content.parts[0].text.strip()

print(f"Assistant: {response_text}")
