import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# Import Gemini module
import google.generativeai as genai

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Create embedding
result = genai.embed_content(
    model="models/embedding-001",
    content="cat",
)

# print embedding
embedding = result['embedding']
print(embedding)
print(f"Shape: {np.array(embedding).shape}")