import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "unofficial_guide"

def retrieve(query, k=4):
    """Return top-k chunks most relevant to the query."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": round(results["distances"][0][i], 3)
        })
    return chunks


if __name__ == "__main__":
    test_queries = [
        "What medicine should I pack for my dorm?",
        "How do I deal with a bad roommate?",
        "How do I make friends if I'm shy?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        chunks = retrieve(query)
        for chunk in chunks:
            print(f"[{chunk['distance']}] ({chunk['source']})")
            print(chunk['text'][:200])
            print()