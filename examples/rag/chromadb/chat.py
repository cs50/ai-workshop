import argparse
import os

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent

from config import CHROMA_DIR, COLLECTION_NAME, INSTRUCTIONS, N_RESULTS

# Parse command-line arguments
parser = argparse.ArgumentParser(description="CS50 RAG Chat")
parser.add_argument("-v", "--verbose", action="store_true", help="Show retrieved chunks in terminal output")
args = parser.parse_args()


# Format a chunk's metadata as a clickable YouTube URL with the lecture name
def format_source(metadata):

    video_id = metadata["video_id"]
    start = metadata["start_time"]
    lecture = metadata["lecture_name"]
    url = f"https://www.youtube.com/watch?v={video_id}&t={start}s"
    return f"  {lecture} @ {start}s — {url}"


# Query ChromaDB for the most relevant chunks matching the user's question
def retrieve(collection, query, n_results=N_RESULTS):

    results = collection.query(query_texts=[query], n_results=n_results)
    return list(zip(results["documents"][0], results["metadatas"][0]))


# Combine retrieved chunks into a numbered context string for the LLM prompt,
# labeling each chunk with its lecture name and time range
def build_context(results):

    parts = []
    for i, (text, meta) in enumerate(results, 1):

        lecture = meta["lecture_name"]
        start = meta["start_time"]
        end = meta["end_time"]
        parts.append(f"[{i}] {lecture} ({start}s–{end}s):\n{text}")

    return "\n\n".join(parts)


# Format all unique source references, sorted by lecture name then start time
def format_sources(results):

    seen = set()
    unique = []

    # Deduplicate sources that share the same video ID and start time
    for _, meta in results:

        key = (meta["video_id"], meta["start_time"])
        if key not in seen:
            seen.add(key)
            unique.append(meta)

    # Sort by lecture name first, then by start time within each lecture
    unique.sort(key=lambda m: (m["lecture_name"], m["start_time"]))
    return "\n".join(format_source(m) for m in unique)


# Print the retrieved chunks to the terminal (used with --verbose flag)
def display_chunks(results):

    print(f"\n{'='*60}")
    print(f"Retrieved {len(results)} chunks:")
    print(f"{'='*60}")

    for i, (text, meta) in enumerate(results, 1):

        lecture = meta["lecture_name"]
        start = meta["start_time"]
        end = meta["end_time"]
        print(f"\n[{i}] {lecture} ({start}s–{end}s)")
        print(f"{'-'*60}")
        print(text)

    print(f"{'='*60}")


# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Connect to the persistent ChromaDB database and load the collection
abs_chroma_dir = os.path.join(os.path.dirname(__file__), CHROMA_DIR)
chroma_client = chromadb.PersistentClient(path=abs_chroma_dir)
collection = chroma_client.get_collection(name=COLLECTION_NAME)
print(f"Loaded collection '{COLLECTION_NAME}' ({collection.count()} chunks)")

# Store the previous response ID to maintain conversation context across turns
previous_response_id = None

# Start an infinite loop to continually accept user input and generate responses
try:
    while True:

        # Prompt the user for a question
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue

        # Step 1: Retrieve the most relevant chunks from ChromaDB
        results = retrieve(collection, user_input)

        # If --verbose flag is set, display the raw retrieved chunks
        if args.verbose:
            display_chunks(results)

        # Step 2: Build the prompt by combining retrieved context with the user's question
        context = build_context(results)
        prompt = (
            "Answer the question using the following lecture transcript excerpts.\n"
            "Cite which lecture and time range your answer comes from.\n\n"
            f"{context}\n\n"
            f"Question: {user_input}"
        )

        # Step 3: Send the prompt to the model with streaming enabled
        response_stream = openai_client.responses.create(
            model="gpt-5.2",
            instructions=INSTRUCTIONS,
            input=prompt,
            previous_response_id=previous_response_id,
            stream=True,
        )

        # Print the assistant's response incrementally as it streams
        print("\nAssistant: ", end="", flush=True)

        # Initialize a variable to capture the completed response
        completed_response = None

        # Iterate over each event in the streamed response
        for event in response_stream:
            if isinstance(event, ResponseTextDeltaEvent):

                # Print the current delta of the response, without adding a new line
                print(event.delta, end="", flush=True)

            # Capture the final response object when streaming completes
            if event.type == "response.completed":
                completed_response = event.response

        # Step 4: Display source references as clickable YouTube links
        print(f"\n\nSources:")
        print(format_sources(results))

        # Save the response ID so the next turn continues the conversation
        if completed_response:
            previous_response_id = completed_response.id

except (KeyboardInterrupt, EOFError):
    print("\nGoodbye!")
