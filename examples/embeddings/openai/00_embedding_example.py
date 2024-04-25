import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# Import the OpenAI module to use OpenAI's API
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Create an embedding for the input text "cat" using the specified model "text-embedding-3-small"
response = client.embeddings.create(
    input="cat",
    model="text-embedding-3-small"
)

# Print the embedding for the input text from the response
embedding = response.data[0].embedding
print(embedding)
print(f"Shape: {np.array(embedding).shape}")