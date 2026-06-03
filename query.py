import os
from groq import Groq
from retrieve import retrieve
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful college survival guide assistant.
Answer the user's question using ONLY the information provided in the context below.
Do not use any outside knowledge — if the context doesn't contain enough information to answer, say "I don't have enough information on that in my documents."
At the end of your answer, always list the sources you drew from under a "Sources:" heading."""

def ask(question):
    """Retrieve relevant chunks and generate a grounded answer."""
    chunks = retrieve(question, k=4)

    # Build context string from retrieved chunks
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n[{i+1}] (Source: {chunk['source']})\n{chunk['text']}\n"

    prompt = f"""Context:
{context}

Question: {question}

Answer using only the context above. Cite sources at the end."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    sources = list(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    test_questions = [
        "What medicine should I pack for my dorm?",
        "What free stuff can I get as a college student?",
        "What is the best pizza place on campus?"  # out-of-scope test
    ]

    for q in test_questions:
        print(f"\nQuestion: {q}")
        print("=" * 60)
        result = ask(q)
        print(result["answer"])
        print()