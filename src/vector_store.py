import os
import shutil
from typing import List
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings 
from langchain_core.documents import Document

from src.document_loader import process_pdf, FILE_PATH, FILE_NAME

FILE_PATH = FILE_PATH
DB_PATH = r"../chroma_db/"

EMBEDDING_MODEL: str = "nomic-embed-text"

def create_embeddings() -> OllamaEmbeddings:
    ollama_url = os.environ.get("OLLAMA_BASE_URL", "https://localhost:11434")
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=ollama_url)

def create_vector_db(chunks: List[Document], persist_directory: str=DB_PATH) -> Chroma:
    print(f"Initializing ChromaDB at: {persist_directory}...")
    if os.path.exists(persist_directory):
        print("Directory found. Clearing for fresh ingestion")
        shutil.rmtree(persist_directory)

    embeddings = create_embeddings()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    print("Succes! Vector  saved to disk")
    return db

def get_vector_store(persist_directory:str = DB_PATH) -> Chroma:
    embeddings = create_embeddings()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )


if __name__ == "__main__":
    try:
        print("Starting vector db Ingestion and Search Test..")

        #step1: geting the chunks from the document loader module
        print("\t\t\tStep 1: Extracting text chunks from pdf...")
        chunks: List[Document] = process_pdf(FILE_PATH, FILE_NAME)

        #step2: store in ChromaDB
        print("\t\t\tStep 2: Storing the chunks in vector db...")
        db = create_vector_db(chunks)

        #step3: Perform semantic search test
        print("\t\t\tStep 3: Testing Semantic Retrieval")
        test_query = "Who is Nandi?"
        print(f"User: {test_query}")


        results = db.similarity_search(test_query, k=3)

        print("\nTop Match Found in the Database: ")
        print("="*60)
        if results:
            print(results[0].page_content)
            print("="*60)
            print(f"Source Metadata: {results[0].metadata}")
        else:
            print("No results found")


    except Exception as e:
        print(f"Error: {e} testing failed for vector db")
