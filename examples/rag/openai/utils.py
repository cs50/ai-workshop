from openai import OpenAI

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
