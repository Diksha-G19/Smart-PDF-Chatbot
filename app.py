import streamlit as st

from pdf_processor import extract_text_from_pdf


# Page configuration
st.set_page_config(
    page_title="Smart PDF Chatbot",
    page_icon="📚",
    layout="wide"
)


# Title
st.title("Smart PDF Chatbot")

st.write(
    "Upload a PDF document and extract its text for processing."
)


# PDF uploader
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"PDF uploaded successfully: {uploaded_file.name}")

    # Extract text
    pages = extract_text_from_pdf(uploaded_file)

    # Basic information
    st.subheader("PDF Information")

    st.write(f"**File name:** {uploaded_file.name}")
    st.write(f"**Number of pages:** {len(pages)}")

    # Check whether text was extracted
    if pages:

        st.success("Text extracted successfully!")

        # Display first page
        st.subheader("Extracted Text")

        first_page = pages[0]

        st.write(
            f"**Page {first_page['page_number']}**"
        )

        st.text_area(
            "Extracted content:",
            first_page["text"],
            height=300
        )

    else:

        st.warning(
            "No text could be extracted from this PDF. "
            "The PDF may contain scanned images instead of selectable text."
        )