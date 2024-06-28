from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


response = client.embeddings.create(
    input="cat",
    model="text-embedding-3-small"
)


embedding = response.data[0].embedding
print(embedding)
print(f"Shape: {np.array(embedding).shape}")
