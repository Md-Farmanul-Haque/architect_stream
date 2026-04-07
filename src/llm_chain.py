from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


from src.vector_store import get_vector_store

LLM_MODEL = "llama3"

def get_llm():
    ollama_url = os.environ.get("OLLAMA_BASE_URL", "https://localhost:11434")
    return ChatOllama(model=LLM_MODEL, temperature=0.8, base_url=ollama_url) # temparature maintains factual correctness


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    # 2. Define the exact instructions for Llama 3
    template = """You are an intelligent AI assistant. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer based on the context, just say that you don't know. Do not make up information.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


if __name__ == "__main__":
    try:
        print("--- Testing the Full RAG Chain ---")
        
        # Initialize the chain
        chain = build_rag_chain()
        
        test_query = "Who is Sati?"
        print(f"\nUser: {test_query}")
        print("Llama 3 is thinking... (This might take a moment on the first run)\n")
        
        # Invoke the chain to get the final answer
        response = chain.invoke(test_query)
        
        print("AI Response:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError in LLM Chain: {e}")