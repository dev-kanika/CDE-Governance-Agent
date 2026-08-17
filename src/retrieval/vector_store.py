from pathlib import Path
import chromadb

from chunker import extract_documents, create_chunks


DB_PATH = Path("data/chroma_db")


documents = extract_documents()
chunks = create_chunks(documents)

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="fdic_documents"
)

collection.upsert(
    ids=[
        f"{chunk['source']}_{chunk['page']}_{i}"
        for i, chunk in enumerate(chunks)
    ],
    documents=[chunk["text"] for chunk in chunks],
    metadatas=[
        {
            "source": chunk["source"],
            "page": chunk["page"],
        }
        for chunk in chunks
    ],
)

print(f"Stored {collection.count()} chunks in Chroma.")