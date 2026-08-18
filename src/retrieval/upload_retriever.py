import uuid

import chromadb

from retrieval.chunker import create_chunks


def retrieve_uploaded_evidence(
    documents,
    question,
    n_results=5
):

    chunks = create_chunks(documents)

    if not chunks:
        return []

    client = chromadb.EphemeralClient()

    collection_name = f"uploaded_{uuid.uuid4().hex}"

    collection = client.create_collection(
        name=collection_name
    )

    collection.add(
        ids=[
            f"chunk_{i}"
            for i in range(len(chunks))
        ],
        documents=[
            chunk["text"]
            for chunk in chunks
        ],
        metadatas=[
            {
                "source": chunk["source"],
                "page": chunk["page"],
            }
            for chunk in chunks
        ],
    )

    results = collection.query(
        query_texts=[question],
        n_results=min(
            n_results,
            len(chunks)
        ),
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    evidence = []

    for i, text in enumerate(
        results["documents"][0]
    ):
        evidence.append({
            "text": text,
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i],
        })

    return evidence