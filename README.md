# Smart PDF Chatbot

A Retrieval-Augmented Generation (RAG) application that lets users
upload PDF documents and ask questions about their content. The
application extracts text from the uploaded PDF, splits it into smaller
chunks, converts the chunks into embeddings, stores them in a FAISS
vector store, retrieves relevant passages for a question, and uses
Google Gemini to generate a grounded answer.

## Features

-   Upload and process PDF documents.
-   Extract text from PDF pages.
-   Split extracted text into smaller chunks for retrieval.
-   Generate embeddings for document chunks.
-   Store and search embeddings using FAISS.
-   Ask natural-language questions about the uploaded document.
-   Generate answers using Google Gemini based on retrieved context.
-   Display source-page information alongside the answer.
-   Present answers in readable Markdown format.

## How It Works

The application follows this RAG workflow:

1.  **PDF Upload** -- The user uploads a PDF through the Streamlit
    interface.
2.  **Text Extraction** -- Text is extracted from the PDF, including
    page information.
3.  **Text Chunking** -- The extracted text is divided into smaller,
    manageable chunks.
4.  **Embedding Generation** -- Each chunk is converted into a numerical
    vector using an embedding model.
5.  **Vector Storage** -- The vectors are stored in a FAISS vector
    store.
6.  **Question Processing** -- The user's question is converted into an
    embedding.
7.  **Semantic Retrieval** -- FAISS retrieves the chunks most relevant
    to the question.
8.  **Answer Generation** -- The retrieved context is sent to Google
    Gemini to generate an answer.
9.  **Source Display** -- The application displays the answer and
    available source-page references.

## Technology Stack

  Component               Technology
  ----------------------- ------------------------------------------
  User interface          Streamlit
  Programming language    Python
  PDF processing          PyMuPDF / project PDF extraction library
  RAG orchestration       LangChain
  Embeddings              Configured embedding model
  Vector database         FAISS
  Large language model    Google Gemini
  Environment variables   python-dotenv

> The exact embedding model and package versions are defined by the
> project's source code and `requirements.txt`.

## Project Structure

``` text
Smart-PDF-Chatbot/
├── app.py                 # Streamlit application and user interface
├── pdf_processor.py       # PDF text extraction and processing
├── rag_pipeline.py        # Chunking, retrieval, and answer generation
├── embedding_test.py      # Embedding model test script
├── requirements.txt       # Python dependencies
├── .env                   # API key configuration (do not commit)
├── .gitignore             # Files excluded from Git
├── data/                  # Project data, if used
└── README.md              # Project documentation
```

## Getting Started

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Smart-PDF-Chatbot
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt and run:

``` cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root and add the Google Gemini API
key using the environment-variable name expected by the application.

For example, if the code reads `GOOGLE_API_KEY`:

``` env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Check `rag_pipeline.py` or the relevant configuration code to confirm
the exact variable name. Do not share your API key or commit the `.env`
file.

### 5. Run the application

``` bash
streamlit run app.py
```

Open the local URL printed in the terminal, usually:

``` text
http://localhost:8501
```

## Using the Application

1.  Start the Streamlit application.
2.  Upload a PDF document using the upload control.
3.  Wait for the document-processing and indexing steps to complete.
4.  Enter a question related to the uploaded document.
5.  Review the generated answer.
6.  Check the displayed source-page reference to identify where the
    information came from.

For best results, use text-based PDFs. Scanned PDFs may require OCR if
the current PDF extraction implementation cannot read their text.

## Configuration and Security

-   Keep API keys in `.env` rather than hard-coding them in Python
    files.
-   Ensure `.env` is listed in `.gitignore`.
-   Do not commit your virtual environment, cache files, or private
    documents.
-   If an API key is accidentally exposed, revoke it and create a
    replacement.

Recommended `.gitignore` entries:

``` gitignore
.env
venv/
__pycache__/
*.py[cod]
.streamlit/secrets.toml
```

## Troubleshooting

### Missing dependency

Activate the project's virtual environment and install the dependencies:

``` bash
python -m pip install -r requirements.txt
```

### Gemini API or quota error

Check that the API key is valid, the environment variable name matches
the code, and the selected model is available to your API account.
Temporary service errors and quota limits may require waiting before
retrying.

### Streamlit application is already running

If the terminal is still running the app, open the local URL shown
there. To stop the app, press `Ctrl + C` in that terminal.

### PDF text is not extracted

Try a text-based PDF. A scanned or image-only PDF may need OCR support.

## Current Project Scope

This project demonstrates a basic document-question-answering workflow
using Retrieval-Augmented Generation. It is intended as an educational
prototype. The quality of answers depends on the PDF text extraction,
chunking, retrieval results, embedding model, and LLM response.

## Future Enhancements

-   Display retrieved text chunks and their similarity scores.
-   Support multiple PDF documents in one session.
-   Add OCR for scanned PDFs.
-   Improve conversation history and follow-up questions.
-   Add persistent document indexing to avoid unnecessary re-embedding.
-   Improve handling of API failures and retrieval edge cases.
-   Add evaluation tests for answer relevance and grounding.

## License

Add a license if you intend to distribute or reuse this project
publicly. Until a license is added, all rights are reserved by the
project owner.
