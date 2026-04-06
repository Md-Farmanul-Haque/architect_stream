import streamlit as st
import os

from src.document_loader import process_pdf, FILE_NAME, FILE_PATH
from src.vector_store import create_vector_db
from src.llm_chain import build_rag_chain

st.set_page_config(page_title="Architect-Stream", page_icon="('_')", layout="centered")

st.title("Architect-Stream")
st.markdown("Your Automated Mentor")
st.divider()


#Session management!
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role":"assistant", "content":"Hello! Upload document to the sidebar to get started!"})


if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None


#Sidebar issue fixture
with st.sidebar:
    st.header("Document Ingestion")

    uploaded_file = st.file_uploader("Upload the File here!",type=["pdf"])

    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Processing PDF and building Vector Database... This might take a moment"):
                try:
                    temp_dir = "temp_documents"
                    os.makedirs(temp_dir, exist_ok = True)
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    chunks = process_pdf(temp_file_path, uploaded_file.name)

                    create_vector_db(chunks)


                    st.session_state.rag_chain = build_rag_chain()

                    st.success(f"Successfully processed, '{uploaded_file.name}' !")
                except Exception as e:
                    st.error(f"Error processing document {e}")
        else:
            st.warning("Please upload a PDF file !")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Capture user input
if user_input := st.chat_input("Ask a question about your architecture or code!"):
    
    # 1. Print the user's message to the screen and save to memory
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Check if the database has been built yet
    if st.session_state.rag_chain is None:
        # If they haven't uploaded a document, give them a warning instead of crashing
        with st.chat_message("assistant"):
            warning_msg = "Please upload and process a document in the sidebar first!"
            st.warning(warning_msg)
            st.session_state.messages.append({"role": "assistant", "content": warning_msg})

    else:
        # 3. Pass the question to Llama 3 and ChromaDB
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and thinking..."):
                try:
                    response = st.session_state.rag_chain.invoke(user_input)
                    st.markdown(response)
                    
                    # Save AI response to memory
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"An error occurred: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            
