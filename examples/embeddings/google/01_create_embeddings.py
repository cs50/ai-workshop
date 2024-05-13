import json
import os
from dotenv import load_dotenv
load_dotenv()

# Import Gemini module
import google.generativeai as genai

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# ==========================================
# embeddings given file i.e whole ai.txt file
# ==========================================

# helper function
def embed_chunk(chunk, model="models/embedding-001"):
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

# Open file
FILE_PATH = "../../../data/transcripts/ai.txt"
with open(FILE_PATH, 'r') as f:

    raw_data = f.read() # read whole file

    # split data into chunks of 500 chars
    chunks = [raw_data[i:i+500] for i in range(0, len(raw_data), 500)]

    embeddings = {} # dictionary contain raw chunk: corresponding embedding

    # embed each chunk in chunks
    print("Creating embeddings...")
    for chunk in chunks:
        embedding = embed_chunk(chunk)
        embeddings[chunk] = embedding

    # saving: write to file name 'embeddings.jsonl'
    print("Write embeddings to file...")
    with open('embeddings.jsonl', 'w') as f:
        for chunk, embedding in embeddings.items():
            f.write((f'{{"text": {json.dumps(chunk)}, "embedding": {embedding}}}\n'))

    print('Written to file.')