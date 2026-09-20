import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

FAISS_INDEX_PATH = "faiss_index"

def create_and_save_vector_store(chunks):
    """Converts text chunks into embeddings and stores them in FAISS."""
    print("Generating embeddings and building FAISS vector store...")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"FAISS vector store saved successfully to {FAISS_INDEX_PATH}/")
    return vector_store

def load_vector_store():
    """Loads an existing FAISS database from the local directory."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError("FAISS index not found. Please run ingestion first.")
        
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    return vector_store