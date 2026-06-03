import os

DOCUMENTS_DIR = "documents"

def load_documents():
    """Load all .txt and .md files from the documents/ folder."""
    documents = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            cleaned = clean_text(raw_text)

            documents.append({
                "source": filename,
                "text": cleaned
            })
            print(f"Loaded: {filename} ({len(cleaned)} chars)")

    return documents


def clean_text(text):
    """Remove noise from raw document text."""
    import re

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove HTML tags if any snuck in
    text = re.sub(r"<[^>]+>", "", text)

    # Remove lines that are just whitespace
    lines = [line for line in text.split("\n") if line.strip()]

    # Collapse multiple blank lines into one
    cleaned = "\n".join(lines)

    return cleaned.strip()


if __name__ == "__main__":
    docs = load_documents()
    print(f"\nTotal documents loaded: {len(docs)}")
    print("\n--- Sample from first document ---")
    print(docs[0]["source"])
    print(docs[0]["text"][:300])