import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env from the backend root folder before importing services
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ingestion import process_document
from app.vector_pipeline import create_and_save_vector_store
from app.graph_pipeline import create_and_store_knowledge_graph
from app.retrieval import generate_hybrid_response

app = FastAPI(title="Customer Support RAG API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Receives a PDF upload, saves it locally, and triggers the full pipeline:
    PDF Extraction -> Chunking -> FAISS Vector DB -> Neo4j Knowledge Graph
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, file.filename)
    
    # Save the incoming PDF file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Process chunks and populate both databases
    try:
        chunks = process_document(file_path)
        create_and_save_vector_store(chunks)
        create_and_store_knowledge_graph(chunks)
        
        return {
            "status": "success", 
            "message": f"Successfully ingested {file.filename} into both FAISS and Neo4j."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_with_agent(request: ChatRequest):
    """
    Executes hybrid retrieval (FAISS + Neo4j) and returns the generated answer.
    """
    try:
        answer = generate_hybrid_response(request.message)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))