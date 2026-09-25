import streamlit as st

from pdf_processor import extract_text_from_pdf, create_chunks
from rag_pipeline import create_vector_store, search_vector_store


st.set_page_config(
    page_title="Smart PDF Chatbot",
    page_icon="📚",
    layout="wide"
)


st.title("Smart PDF Chatbot")

st.write(
    "Upload a PDF and ask questions about its content."
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"PDF uploaded successfully: {uploaded_file.name}"
    )

    # -----------------------------------
    # STEP 1: Extract text
    # -----------------------------------

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

        # -----------------------------------
        # STEP 2: Create chunks
        # -----------------------------------

        chunks = create_chunks(pages)

        st.subheader("Text Chunking")

        st.write(
            f"**Number of chunks:** {len(chunks)}"
        )

        # -----------------------------------
        # STEP 3: Create FAISS vector store
        # -----------------------------------

        with st.spinner(
            "Creating FAISS vector database..."
        ):

            vector_store = create_vector_store(chunks)

        st.success(
            "FAISS vector database created successfully!"
        )

        # -----------------------------------
        # STEP 4: Ask question
        # -----------------------------------

        st.subheader("Ask a Question")

        question = st.text_input(
            "Enter your question:"
        )

        if question:

            with st.spinner(
                "Searching the document..."
            ):

                results = search_vector_store(
                    vector_store,
                    question,
                    k=3
                )

            st.subheader("Retrieved Information")

            st.write(
                f"Found {len(results)} relevant chunks."
            )

            for i, result in enumerate(
                results,
                start=1
            ):

                page_number = result.metadata.get(
                    "page_number",
                    "Unknown"
                )

                with st.expander(
                    f"Result {i} — Page {page_number}"
                ):

                    st.write(result.page_content)

    else:

        st.warning(
            "No text could be extracted from this PDF."
        )