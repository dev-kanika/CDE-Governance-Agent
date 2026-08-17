from pathlib import Path
import re
import pymupdf


DOCUMENTS_FOLDER = Path("data/documents")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_documents():
    documents = []

    for pdf_path in DOCUMENTS_FOLDER.glob("*.pdf"):
        pdf = pymupdf.open(pdf_path)

        for page_number, page in enumerate(pdf, start=1):
            text = clean_text(page.get_text())

            if text:
                documents.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "text": text,
                })

        pdf.close()

    return documents


def create_chunks(documents, chunk_size=1000):
    chunks = []

    for document in documents:
        paragraphs = re.split(r"(?<=[.!?])\s+", document["text"])

        current_chunk = ""

        for paragraph in paragraphs:
            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += " " + paragraph
            else:
                if current_chunk:
                    chunks.append({
                        "source": document["source"],
                        "page": document["page"],
                        "text": current_chunk.strip(),
                    })

                current_chunk = paragraph

        if current_chunk:
            chunks.append({
                "source": document["source"],
                "page": document["page"],
                "text": current_chunk.strip(),
            })

    return chunks


documents = extract_documents()
chunks = create_chunks(documents)

print(f"Created {len(chunks)} chunks.")

for chunk in chunks[:3]:
    print("\n---")
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print(chunk["text"][:500])