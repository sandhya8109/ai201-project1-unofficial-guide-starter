from ingest import load_documents

CHUNK_SIZE = 400
OVERLAP = 80


def chunk_text(text, source):
    """Split text into overlapping chunks, trying paragraph boundaries first."""
    chunks = []

    # Split into paragraphs first
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    current_chunk = ""

    for paragraph in paragraphs:
        # If a single paragraph is already longer than CHUNK_SIZE, split it by characters
        if len(paragraph) > CHUNK_SIZE:
            # First save whatever we had building up
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # Split long paragraph into character chunks with overlap
            start = 0
            while start < len(paragraph):
                end = start + CHUNK_SIZE
                chunk = paragraph[start:end]
                chunks.append(chunk.strip())
                start += CHUNK_SIZE - OVERLAP

        # If adding this paragraph keeps us under the limit, keep building
        elif len(current_chunk) + len(paragraph) + 1 <= CHUNK_SIZE:
            current_chunk += (" " if current_chunk else "") + paragraph

        # Otherwise save current chunk and start a new one
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Start new chunk with overlap from end of previous
            overlap_text = current_chunk[-OVERLAP:] if len(current_chunk) > OVERLAP else current_chunk
            current_chunk = overlap_text + " " + paragraph

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Attach source to each chunk
    return [{"text": chunk, "source": source} for chunk in chunks if len(chunk) > 30]


def chunk_all_documents(documents):
    """Chunk every document and return a flat list of all chunks."""
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(doc_chunks)
        print(f"{doc['source']}: {len(doc_chunks)} chunks")
    return all_chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_all_documents(docs)

    print(f"\nTotal chunks: {len(chunks)}")
    print("\n--- 5 sample chunks ---")
    import random
    for sample in random.sample(chunks, 5):
        print(f"\nSource: {sample['source']}")
        print(f"Length: {len(sample['text'])} chars")
        print(f"Text: {sample['text']}")
        print("-" * 40)