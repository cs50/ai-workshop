# Configuration: change these to customize the ingestion and chat behavior

# Path to the SRT subtitle files
SRT_DIR = "../../../data/transcripts/srt/"

# CSV file mapping YouTube video IDs and lecture names to SRT filenames
INDEX_CSV = "../../../data/transcripts/srt/index.csv"

# Directory for the persistent ChromaDB database
CHROMA_DIR = "../../../data/chromadb"

# Name of the ChromaDB collection to store lecture chunks
COLLECTION_NAME = "cs50_lectures"

# OpenAI embedding model used by ChromaDB for both ingestion and retrieval
EMBEDDING_MODEL = "text-embedding-3-large"

# Chunking parameters (in seconds):
# Each chunk will span at least CHUNK_MIN_DURATION but not exceed CHUNK_MAX_DURATION
CHUNK_MIN_DURATION = 30
CHUNK_MAX_DURATION = 40

# System prompt that sets the context for the chatbot
INSTRUCTIONS = (
    "You are a friendly and supportive teaching assistant for CS50. "
    "You are also a rubber duck. "
    "Answer student questions only about CS50 and the field of computer science; "
    "Do not answer questions about unrelated topics. "
    "Do not provide full answers to problem sets, as this would violate academic honesty. "
    "When answering, use the provided lecture transcript excerpts as context. "
    "Always reference which lecture and timestamp your answer comes from."
)

# Number of chunks to retrieve from ChromaDB per query
N_RESULTS = 5
