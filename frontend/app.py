import os
import streamlit as st
import requests

# Defaults to localhost for local testing, but can be overridden by Docker
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Customer Support RAG", layout="wide")
st.title("🎧 AI Customer Support Agent")
st.caption("Hybrid RAG: FAISS Vector Store + Neo4j Knowledge Graph")

# Sidebar: Upload & Ingestion Controls
with st.sidebar:
    st.header("📄 Knowledge Ingestion")
    st.write("Upload a PDF to update the agent's knowledge base.")
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if st.button("Ingest Document", use_container_width=True):
        if uploaded_file is None:
            st.warning("Please upload a PDF file first.")
        else:
            with st.spinner("Uploading, chunking, embedding, and building graph..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/ingest", files=files)
                    
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Document ingested successfully!"))
                    else:
                        st.error(f"Error {response.status_code}: {response.json().get('detail', 'Failed to ingest.')}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI. Make sure the backend server is running on port 8000.")

# Main Area: Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your support agent. Upload a document from the sidebar or ask a question."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consulting Vector DB and Knowledge Graph..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": prompt}
                )
                
                if response.status_code == 200:
                    answer = response.json().get("response", "No response generated.")
                else:
                    detail = response.json().get("detail", "Error processing request.")
                    answer = f"⚠️ **Backend Error ({response.status_code}):** {detail}"
            except requests.exceptions.ConnectionError:
                answer = "⚠️ **Connection Error:** Backend server is not reachable at http://localhost:8000."

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})