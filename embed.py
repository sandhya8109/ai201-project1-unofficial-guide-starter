import chromadb
from sentence_transformers import SentenceTransformer
from chunk import chunk_all_documents
from ingest import load_documents

COLLECTION_NAME = "unofficial_guide"

def build_vector_store():
    """Embed all chunks and store them in ChromaDB."""

    # Load and chunk documents
    print("Loading documents...")
    docs = load_documents()
    print("Chunking documents...")
    chunks = chunk_all_documents(docs)
    print(f"\nTotal chunks to embed: {len(chunks)}")

    # Load embedding model (downloads once, cached after)
    print("\nLoading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB (saves to disk in ./chroma_db/)
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete collection if it already exists (so we can re-run cleanly)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")
    except:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    # Embed and store in batches
    print("Embedding and storing chunks...")
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s} for s in sources]
    )

    print(f"\nDone! {collection.count()} chunks stored in ChromaDB.")


if __name__ == "__main__":
    build_vector_store()