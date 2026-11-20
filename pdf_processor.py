from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter



def extract_text_from_pdf(pdf_file):

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
