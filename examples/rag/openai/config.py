from openai import OpenAI

# Configuration: change these to customize the assistant's behavior and data sources
FILES_DIR = "../../../data/transcripts/"
VECTOR_STORE_NAME = "CS50 Lecture Captions"
INSTRUCTIONS = (
    "You are a friendly and supportive teaching assistant for CS50. "
    "You are also a rubber duck. "
    "Answer student questions only about CS50 and the field of computer science; "
    "Do not answer questions about unrelated topics. "
    "Do not provide full answers to problem sets, as this would violate academic honesty."
)

def clean_up(client: OpenAI, vector_store_id, file_ids):
    """Delete the vector store and uploaded files."""

    print("\nCleaning up resources...")
    client.vector_stores.delete(vector_store_id)
    for file_id in file_ids:
        try:
            client.files.delete(file_id)
        except Exception as e:
            print(f"Failed to delete file {file_id}: {e}")
    print("Done.")
