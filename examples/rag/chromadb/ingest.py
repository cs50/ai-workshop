import csv
import os
import re

import chromadb

from config import (
    CHUNK_MAX_DURATION,
    CHUNK_MIN_DURATION,
    CHROMA_DIR,
    COLLECTION_NAME,
    INDEX_CSV,
    SRT_DIR,
)


# Convert an SRT timestamp string (e.g., "00:02:03,959") to total seconds
def parse_timestamp(ts):

    match = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", ts.strip())
    h, m, s, ms = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
    return h * 3600 + m * 60 + s + ms / 1000


# Parse an SRT file and return a list of subtitle entries,
# each with 'start' (seconds), 'end' (seconds), and 'text'
def parse_srt(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on blank lines to get individual subtitle blocks
    # Each block has: sequence number, timestamp line, and caption text
    blocks = re.split(r"\n\s*\n", content.strip())
    entries = []

    for block in blocks:

        lines = block.strip().split("\n")

        # A valid SRT block needs at least 3 lines: index, timestamp, and text
        if len(lines) < 3:
            continue

        # Parse the timestamp line (e.g., "00:02:03,959 --> 00:02:03,970")
        timestamp_line = lines[1]
        match = re.match(r"(.+?)\s*-->\s*(.+)", timestamp_line)
        if not match:
            continue

        start = parse_timestamp(match.group(1))
        end = parse_timestamp(match.group(2))

        # Join all remaining lines as the caption text
        text = " ".join(lines[2:]).strip()

        if text:
            entries.append({"start": start, "end": end, "text": text})

    return entries


# Merge consecutive subtitle entries into time-based chunks.
# Each chunk spans at least min_duration seconds but does not exceed max_duration.
def chunk_entries(entries, min_duration=CHUNK_MIN_DURATION, max_duration=CHUNK_MAX_DURATION):

    chunks = []
    if not entries:
        return chunks

    i = 0
    while i < len(entries):

        # Start a new chunk with the current entry
        chunk_start = entries[i]["start"]
        chunk_end = entries[i]["end"]
        chunk_texts = [entries[i]["text"]]
        i += 1

        # Keep adding entries until we meet the duration constraints
        while i < len(entries):

            candidate_end = entries[i]["end"]
            candidate_duration = candidate_end - chunk_start

            # Stop if adding this entry would exceed max_duration
            if candidate_duration > max_duration:
                break

            chunk_texts.append(entries[i]["text"])
            chunk_end = candidate_end
            i += 1

            # Close the chunk once we've reached min_duration
            if chunk_end - chunk_start >= min_duration:
                break

        chunks.append({
            "start": chunk_start,
            "end": chunk_end,
            "text": " ".join(chunk_texts),
        })

    return chunks


# Load the index CSV that maps SRT filenames to YouTube video IDs and lecture names
def load_index(index_path):

    index = {}
    with open(index_path, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        # Build a dictionary keyed by SRT filename
        for row in reader:
            index[row["caption"]] = {
                "video_id": row["id"],
                "lecture_name": row["name"],
            }

    return index


# Resolve paths relative to this script's directory
abs_srt_dir = os.path.join(os.path.dirname(__file__), SRT_DIR)
abs_index_csv = os.path.join(os.path.dirname(__file__), INDEX_CSV)
abs_chroma_dir = os.path.join(os.path.dirname(__file__), CHROMA_DIR)

# Load the lecture index from the CSV file
index = load_index(abs_index_csv)
print(f"Loaded index with {len(index)} lectures")

# Initialize a persistent ChromaDB client (data is saved to disk)
client = chromadb.PersistentClient(path=abs_chroma_dir)

# Delete existing collection if it exists, so we start fresh each time
try:
    client.delete_collection(COLLECTION_NAME)
    print(f"Deleted existing collection '{COLLECTION_NAME}'")
except Exception:
    pass

# Create a new collection using cosine similarity for semantic search
collection = client.create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)
print(f"Created collection '{COLLECTION_NAME}'")

total_chunks = 0

# Process each SRT file listed in the index
for srt_file, meta in sorted(index.items()):

    srt_path = os.path.join(abs_srt_dir, srt_file)
    if not os.path.exists(srt_path):
        print(f"  WARNING: {srt_file} not found, skipping")
        continue

    # Parse the SRT file into individual caption entries
    entries = parse_srt(srt_path)

    # Merge captions into ~30-second chunks
    chunks = chunk_entries(entries)
    print(f"  {meta['lecture_name']}: {len(entries)} captions -> {len(chunks)} chunks")

    # Prepare batch data for ChromaDB: each chunk gets a unique ID, document text, and metadata
    ids = []
    documents = []
    metadatas = []

    for j, chunk in enumerate(chunks):

        chunk_id = f"{srt_file}_{j}"
        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({
            "lecture_name": meta["lecture_name"],
            "video_id": meta["video_id"],
            "start_time": int(chunk["start"]),
            "end_time": int(chunk["end"]),
            "srt_file": srt_file,
        })

    # Add all chunks for this lecture to ChromaDB in one batch
    if ids:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        total_chunks += len(ids)

print(f"\nIngestion complete: {total_chunks} chunks added to '{COLLECTION_NAME}'")
