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


documents = extract_documents()

print(
    f"Extracted {len(documents)} non-empty pages "
    f"from {len(set(d['source'] for d in documents))} PDFs."
)

for document in documents[:3]:
    print("\n---")
    print("Source:", document["source"])
    print("Page:", document["page"])
    print(document["text"][:300])