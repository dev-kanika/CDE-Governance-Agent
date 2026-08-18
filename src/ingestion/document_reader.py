import io
from pathlib import Path

import pymupdf
from docx import Document


def clean_text(text):
    return " ".join(text.split()).strip()


def read_pdf(file_bytes, filename):
    pages = []

    pdf = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    for page_number, page in enumerate(pdf, start=1):
        text = clean_text(page.get_text())

        if text:
            pages.append({
                "source": filename,
                "page": page_number,
                "text": text,
            })

    pdf.close()

    return pages


def read_docx(file_bytes, filename):
    document = Document(
        io.BytesIO(file_bytes)
    )

    pages = []
    current_text = []

    for paragraph in document.paragraphs:

        text = clean_text(paragraph.text)

        if text:
            current_text.append(text)

    combined_text = " ".join(current_text)

    if combined_text:
        pages.append({
            "source": filename,
            "page": 1,
            "text": combined_text,
        })

    return pages


def read_uploaded_document(file_bytes, filename):

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return read_pdf(
            file_bytes,
            filename
        )

    if extension == ".docx":
        return read_docx(
            file_bytes,
            filename
        )

    raise ValueError(
        "Unsupported file type. "
        "Please upload a PDF or DOCX file."
    )