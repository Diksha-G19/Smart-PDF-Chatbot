import streamlit as st

from pdf_processor import extract_text_from_pdf, create_chunks


st.set_page_config(
    page_title="Smart PDF Chatbot",
    page_icon="📚",
    layout="wide"
)


st.title("Smart PDF Chatbot")

st.write(
    "Upload a PDF document and process its content."
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"PDF uploaded successfully: {uploaded_file.name}"
    )

    # Step 1: Extract text
    pages = extract_text_from_pdf(uploaded_file)

    st.subheader("PDF Information")

    st.write(
        f"**File name:** {uploaded_file.name}"
    )

    st.write(
        f"**Number of pages:** {len(pages)}"
    )

    if pages:

        st.success("Text extracted successfully!")

        # Step 2: Create chunks
        chunks = create_chunks(pages)

        st.subheader("Text Chunking")

        st.write(
            f"**Number of chunks created:** {len(chunks)}"
        )

        # Display first few chunks
        for i, chunk in enumerate(chunks[:5], start=1):

            with st.expander(
                f"Chunk {i} — Page {chunk['page_number']}"
            ):

                st.write(chunk["text"])

    else:

        st.warning(
            "No text could be extracted from this PDF."
        )