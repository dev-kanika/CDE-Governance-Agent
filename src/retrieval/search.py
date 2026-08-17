import chromadb
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from tests.rag_questions import questions

DB_PATH = "data/chroma_db"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection("fdic_documents")

for item in questions:
    question = item["question"]
    expected = item["expected"]

    results = collection.query(
        query_texts=[question],
        n_results=1,
        include=["documents", "metadatas", "distances"],
    )

    distance = results["distances"][0][0]
    metadata = results["metadatas"][0][0]

    print("\n" + "=" * 70)
    print("Question :", question)
    print("Expected :", expected)
    print("Distance :", round(distance, 4))
    print("Source   :", metadata["source"])
    print("Page     :", metadata["page"])