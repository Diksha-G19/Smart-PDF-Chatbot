from pypdf import PdfReader


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