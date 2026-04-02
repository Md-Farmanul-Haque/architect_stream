```markdown
# Architect-Stream: Local RAG Technical Mentor

An end-to-end Retrieval-Augmented Generation (RAG) application that acts as an automated technical mentor. Architect-Stream allows users to upload technical PDFs, intelligently parses the information, and enables interactive, context-aware "interviews" regarding the document's content—all running entirely locally without external API dependencies.

## Project Goals
1. **Interactive Document Analysis:** Transform static technical PDFs into dynamic, queryable knowledge bases.
2. **Zero Hallucination:** Ensure the language model grounds its responses *strictly* in the provided document context.
3. **100% Local Execution:** Prioritize data privacy and eliminate API costs by orchestrating open-weights models locally via Ollama.
4. **Architectural Modularity:** Separate ingestion, vector storage, and generation logic into a clean, maintainable backend structure decoupled from the frontend UI.

## Key Learnings & Competencies Demonstrated
Building this project solidified my understanding of modern AI/ML application architecture, specifically:
* **Advanced Data Ingestion:** Managing token limits and context windows using LangChain's recursive text splitting and chunking strategies.
* **Vector Database Management:** Implementing `ChromaDB` for persistent local vector storage, embedding generation, and high-dimensional semantic search.
* **LLM Orchestration:** Designing customized LangChain prompt templates to constrain the LLM's behavior and enforce strict adherence to retrieved context.
* **Full-Stack Prototyping:** Bridging backend machine learning logic with a responsive, user-friendly frontend using `Streamlit`.

## Technology Stack
* **Language:** Python
* **LLM:** Llama 3 (via local Ollama)
* **Framework:** LangChain
* **Vector Database:** ChromaDB
* **Data Ingestion:** PyPDFLoader (langchain-community)
* **Frontend:** Streamlit

## System Architecture & Workflow
1. **Upload:** User provides a technical PDF through the Streamlit interface.
2. **Ingestion & Chunking:** `PyPDFLoader` extracts text; LangChain splits it into manageable, token-optimized chunks.
3. **Embedding & Storage:** Text chunks are converted into mathematical vectors and stored locally in ChromaDB.
4. **Retrieval:** When a user submits a query, the system performs a semantic search against ChromaDB to retrieve the most relevant chunks.
5. **Generation:** The retrieved context and user query are injected into a strict prompt template and sent to the local Llama 3 model, generating an accurate, hallucination-free response.

## Repository Structure
```text
Architect-Stream/
├── app.py                   # Streamlit UI frontend
├── requirements.txt         # Python dependencies
├── src/                     # Backend module
│   ├── __init__.py
│   ├── document_loader.py   # PDF ingestion and chunking logic
│   ├── vector_store.py      # ChromaDB initialization and semantic search
│   └── llm_chain.py         # Llama 3 initialization and prompt engineering
├── chroma_db/               # (Ignored) Persistent local vector database
└── uploads/                 # (Ignored) Temporary PDF storage
```

## Local Setup & Installation

### Prerequisites
1. **Python 3.9+** installed on your machine.
2. **Ollama** installed and running globally. 
   * Download from [ollama.com](https://ollama.com/)
   * Pull the Llama 3 model by running: `ollama run llama3` in your terminal.

### Step-by-Step Installation

**1. Clone the repository**

git clone [REPO_URL](https://github.com/Md-Farmanul-Haque/architect_stream.git)
```
cd Architect-Stream
```

**2. Create a virtual environment**
```cmd
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```cmd
pip install -r requirements.txt
```

## Usage

**1. Start the Streamlit Application**
Ensure your virtual environment is activated and Ollama is running in the background, then execute:
```cmd
streamlit run app.py
```

**2. Interact**
* Open the local URL provided by Streamlit in your browser (usually `http://localhost:8501`).
* Upload a technical PDF using the sidebar.
* Wait for the system to process and embed the document.
* Start asking questions in the chat interface!

## Future Enhancements
* **Multi-Document Support:** Update the ingestion pipeline to handle a directory of PDFs simultaneously.
* **Hybrid Search:** Implement BM25 alongside dense vector retrieval for improved accuracy on keyword-heavy technical queries.
* **Streaming Responses:** Enable real-time token streaming in the Streamlit UI to improve perceived latency.
