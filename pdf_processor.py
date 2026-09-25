from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter



def extract_text_from_pdf(pdf_file):
    """
    Extract text from each page of a PDF file.

    Returns:
        pages: List of dictionaries containing page number and text.
    """

    reader = PdfReader(pdf_file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return pages


def create_chunks(pages):
    """
    Split extracted PDF text into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for page in pages:

        page_chunks = text_splitter.split_text(page["text"])

        for chunk in page_chunks:

            chunks.append({
                "page_number": page["page_number"],
                "text": chunk
            })

    return chunks

"""
Why 1000 and 200?

We're using:
chunk_size = 1000
chunk_overlap = 200

Meaning approximately:
Chunk 1:
characters 1 → 1000
Chunk 2:
characters 801 → 1800
Chunk 3:
characters 1601 → 2600

The overlap helps retain context around chunk boundaries.
These aren't magical values. Later, we can experiment with them
"""