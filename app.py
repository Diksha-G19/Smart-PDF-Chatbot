import streamlit as st

from pdf_processor import extract_text_from_pdf, create_chunks
from rag_pipeline import create_embeddings


st.set_page_config(
    page_title="Smart PDF Chatbot",
    page_icon="📚",
    layout="wide"
)


st.title("Smart PDF Chatbot")

st.write(
    "Upload a PDF and convert its content into "
    "searchable vector representations."
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"PDF uploaded successfully: {uploaded_file.name}"
    )

    # -----------------------------
    # STEP 1: Extract text
    # -----------------------------

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

        # -----------------------------
        # STEP 2: Create chunks
        # -----------------------------

        chunks = create_chunks(pages)

        st.subheader("Text Chunking")

        st.write(
            f"**Number of chunks:** {len(chunks)}"
        )

        # -----------------------------
        # STEP 3: Generate embeddings
        # -----------------------------

        with st.spinner("Generating embeddings..."):

            vectors = create_embeddings(chunks)

        st.success("Embeddings generated successfully!")

        st.subheader("Embeddings")

        st.write(
            f"**Number of embeddings:** {len(vectors)}"
        )

        if vectors:

            st.write(
                f"**Embedding dimension:** {len(vectors[0])}"
            )

            st.write("**First embedding (first 10 values):**")

            st.code(
                str(vectors[0][:10])
            )

        # -----------------------------
        # STEP 4: Show sample chunks
        # -----------------------------

        st.subheader("Sample Chunks")

        for i, chunk in enumerate(chunks[:3], start=1):

            with st.expander(
                f"Chunk {i} — Page {chunk['page_number']}"
            ):

                st.write(chunk["text"])

    else:

        st.warning(
            "No text could be extracted from this PDF."
        )