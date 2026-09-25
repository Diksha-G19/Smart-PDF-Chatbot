import streamlit as st

from pdf_processor import (
    extract_text_from_pdf,
    create_chunks
)

from rag_pipeline import (
    get_embedding_model,
    create_vector_store,
    search_vector_store,
    generate_answer
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart PDF Chatbot",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📚 Smart PDF Chatbot")

st.write(
    "A step-by-step demonstration of "
    "Retrieval-Augmented Generation (RAG)"
)

st.divider()


# --------------------------------------------------
# STEP 1 — PDF UPLOAD
# --------------------------------------------------

st.header("1️⃣ PDF Input")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"PDF uploaded successfully: {uploaded_file.name}"
    )

    st.write(
        f"**File name:** {uploaded_file.name}"
    )


    # --------------------------------------------------
    # STEP 2 — TEXT EXTRACTION
    # --------------------------------------------------

    st.header("2️⃣ Text Extraction")

    with st.spinner("Extracting text from PDF..."):

        pages = extract_text_from_pdf(uploaded_file)

    if not pages:

        st.error(
            "No text could be extracted from this PDF."
        )

        st.stop()


    st.success(
        f"Text extracted successfully from "
        f"{len(pages)} pages."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Number of Pages",
            len(pages)
        )

    with col2:

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        st.metric(
            "Characters Extracted",
            total_characters
        )


    with st.expander("👀 View Extracted Text"):

        for page in pages[:3]:

            st.write(
                f"### Page {page['page_number']}"
            )

            st.text(
                page["text"][:2000]
            )

            st.divider()


    # --------------------------------------------------
    # STEP 3 — TEXT CHUNKING
    # --------------------------------------------------

    st.header("3️⃣ Text Chunking")

    chunks = create_chunks(pages)

    st.success(
        f"Created {len(chunks)} text chunks."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Chunks",
            len(chunks)
        )

    with col2:

        st.write("**Chunk settings**")
        st.write("Chunk size: 1000")
        st.write("Overlap: 200")


    with st.expander("🧩 View Sample Chunks"):

        for i, chunk in enumerate(
            chunks[:3],
            start=1
        ):

            st.write(
                f"### Chunk {i} — Page "
                f"{chunk['page_number']}"
            )

            st.text(
                chunk["text"]
            )

            st.divider()


    # --------------------------------------------------
    # STEP 4 — EMBEDDINGS
    # --------------------------------------------------

    st.header("4️⃣ Text Embeddings")

    embedding_model = get_embedding_model()

    with st.spinner(
        "Converting document chunks into embeddings..."
    ):

        sample_vector = embedding_model.embed_query(
            chunks[0]["text"]
        )

    st.success(
        "Embedding model initialized successfully."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Chunks to Embed",
            len(chunks)
        )

    with col2:

        st.metric(
            "Vector Dimension",
            len(sample_vector)
        )


    with st.expander("🧠 View Sample Embedding"):

        st.write(
            "First 10 values of the first chunk's vector:"
        )

        st.code(
            str(sample_vector[:10])
        )

        st.caption(
            "Each document chunk is converted into "
            "a numerical vector representing its meaning."
        )


    # --------------------------------------------------
    # STEP 5 — FAISS
    # --------------------------------------------------

    st.header("5️⃣ FAISS Vector Store")

    with st.spinner(
        "Creating FAISS vector database..."
    ):

        vector_store = create_vector_store(chunks)

    st.success(
        "FAISS vector store created successfully."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Vectors Stored",
            len(chunks)
        )

    with col2:

        st.write("**Database:** FAISS")
        st.write("**Search type:** Semantic similarity")


    with st.expander("ℹ️ What is happening here?"):

        st.write(
            "The embeddings are stored in FAISS so that "
            "the system can efficiently find document "
            "chunks that are semantically similar to "
            "a user's question."
        )


    st.divider()


    # --------------------------------------------------
    # STEP 6 — USER QUESTION
    # --------------------------------------------------

    st.header("6️⃣ Ask a Question")

    question = st.text_input(
        "Enter a question about your PDF:",
        placeholder="Example: What is this document about?"
    )


    if question:

        # --------------------------------------------------
        # STEP 7 — QUESTION EMBEDDING
        # --------------------------------------------------

        st.header("7️⃣ Question Embedding")

        with st.spinner(
            "Converting question into an embedding..."
        ):

            question_vector = embedding_model.embed_query(
                question
            )

        st.success(
            "Question converted into a vector."
        )

        st.write(
            f"**Question:** {question}"
        )

        st.write(
            f"**Vector dimension:** "
            f"{len(question_vector)}"
        )

        with st.expander("🔢 View Question Vector"):

            st.code(
                str(question_vector[:10])
            )


        # --------------------------------------------------
        # STEP 8 — SEMANTIC RETRIEVAL
        # --------------------------------------------------

        st.header("8️⃣ Semantic Retrieval")

        with st.spinner(
            "Searching FAISS for relevant chunks..."
        ):

            results = search_vector_store(
                vector_store,
                question,
                k=3
            )

        st.success(
            f"Retrieved {len(results)} relevant chunks."
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

                st.write(
                    result.page_content
                )


        st.info(
            "The retrieved chunks will be provided "
            "to Gemini in the next stage."
        )

        # --------------------------------------------------
        # STEP 9 — GEMINI GENERATION
        # --------------------------------------------------

        st.header("9️⃣ Gemini LLM Generation")

        st.write(
            "The retrieved document chunks are provided "
            "to Gemini as context."
        )

        # Show the context sent to Gemini
        with st.expander("📚 View Context Sent to Gemini"):

            for i, result in enumerate(
                results,
                start=1
            ):

                page_number = result.metadata.get(
                    "page_number",
                    "Unknown"
                )

                st.write(
                    f"**Retrieved Chunk {i} — Page {page_number}**"
                )

                st.text(
                    result.page_content
                )

                st.divider()


        with st.spinner(
            "Gemini is generating an answer..."
        ):

            answer = generate_answer(
                question,
                results
            )

        st.success(
            "Answer generated successfully."
        )


        # --------------------------------------------------
        # STEP 10 — FINAL ANSWER
        # --------------------------------------------------

        st.header("🔟 Final Answer")

        st.markdown(
            f"### 🤖 Answer"
        )

        st.write(answer)


        # --------------------------------------------------
        # SOURCES
        # --------------------------------------------------

        st.subheader("📚 Sources")

        source_pages = []

        for result in results:

            page = result.metadata.get(
                "page_number",
                "Unknown"
            )

            if page not in source_pages:
                source_pages.append(page)


        for page in source_pages:

            st.write(
                f"📄 Page {page}"
            )