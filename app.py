import streamlit as st

st.set_page_config(page_title="Architect-Stream", page_icon="****", layout="centered")

st.title("Architect-Stream")
st.markdown("Your Automated Mentor")
st.divider()


with st.sidebar:
    st.header("Document Ingestion")
    st.file_uploader("Upload the files here", type=["pdf"])
    st.button("Process Document")



st.chat_message("Assistant").write("Hello upload any document to the sidebar, to get started!")

if user_input := st.chat_input("Ask a question about your architecture or code!"):
    st.chat_message("user").write(user_input)