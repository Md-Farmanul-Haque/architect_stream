import os 
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


#Global configuration and constants 
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
FILE_NAME: str = "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.pdf"
FILE_PATH: str = os.path.join(CURR_DIR, "..", "documents", FILE_NAME)

# validating and loading document
def validate_load_doc(file_path: str, file_name: str) -> List[Document]:
    if os.path.exists(file_path):
        print(f"{file_name}: loading..")
        loader = PyPDFLoader(file_path)
        return loader.load()
    else:
        raise FileNotFoundError(f"{file_name} does not exists")


def text_2_chunk(documents: List[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks =  text_splitter.split_documents(documents)
    return chunks


def process_pdf(file_path:str, file_name:str) -> List[Document]:
    raw_doc = validate_load_doc(file_path, file_name)
    processed_pdf = text_2_chunk(raw_doc, CHUNK_SIZE, CHUNK_OVERLAP)

    return processed_pdf

if __name__ == "__main__":
    chunks: List[Document] = process_pdf(FILE_PATH, FILE_NAME)
    print(f"\nSuccess! Document split into {len(chunks)} chunks.")
        
    if chunks:
        print("\nPreview of Chunk 1:")
        print("-" * 40)
        print(chunks[0].page_content)
        print("-" * 40)
        print(f"Metadata: {chunks[0].metadata}")
        