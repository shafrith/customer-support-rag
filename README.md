# AI Customer Support Agent — Hybrid RAG

A modular, microservices-based **Hybrid RAG customer support agent** that combines semantic vector search with knowledge graph reasoning to provide context-aware answers from uploaded PDF documents.

## 🏗 Architecture & Tech Stack

* **Frontend (UI):** Streamlit
* **Backend (API):** FastAPI, Uvicorn
* **AI Orchestration:** LangChain
* **Vector Database:** FAISS
* **Graph Database:** Neo4j
* **Knowledge Graph:** Neo4j
* **LLM:** OpenAI GPT-3.5-turbo
* **Embeddings:** OpenAI Embeddings
* **Containerization:** Docker, Docker Compose
* **PDF Processing:** PDF text extraction and document chunking

## ✨ Features

### 📄 PDF Knowledge Ingestion

Upload PDF documents through the Streamlit UI.

The ingestion pipeline:

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
 ┌──────────────────┬────────────────────┐
 ↓                  ↓
FAISS              Neo4j
Vector Store       Knowledge Graph
```

### 🔍 Hybrid Retrieval

The system retrieves information from two independent sources:

**FAISS Vector Search**

* Performs semantic similarity search.
* Finds relevant document chunks based on meaning.
* Useful for broader contextual questions.

**Neo4j Knowledge Graph**

* Stores entities and relationships extracted from the documents.
* Uses graph-based retrieval to identify connected information.
* Supports structured relationship-based queries.

### 🧠 Context Fusion

The retrieved information from FAISS and Neo4j is combined before being sent to the LLM.

```text
User Question
      ↓
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
FAISS          Neo4j
Vector         Knowledge
Search         Graph
 ↓              ↓
 └───────┬──────┘
         ↓
  Context Fusion
         ↓
      LLM
         ↓
  Final Answer
```

### 🐳 Microservices Architecture

The application separates the frontend and backend into independent services:

```text
Streamlit Frontend
       ↓
   FastAPI Backend
       ↓
 ┌─────┴──────┐
 ↓            ↓
FAISS       Neo4j
```

Docker Compose manages the services and their communication.

## 📋 Prerequisites

Install the following:

* Docker
* Docker Desktop
* OpenAI API Key
* Neo4j instance

Neo4j can run locally, through Docker, or using Neo4j AuraDB.

## ⚙️ Environment Variables

Create a `.env` file inside the `backend/` directory.

Use the following configuration:

```env
OPENAI_API_KEY=your_openai_api_key

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password

# Optional
NEO4J_DATABASE=
```

Never commit your `.env` file to GitHub.

## 🚀 Running with Docker

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Start the application

Build and start all services:

```bash
docker compose up --build -d
```

### 3. Access the application

**Frontend:**

```text
http://localhost:8501
```

**Backend API documentation:**

```text
http://localhost:8000/docs
```

## 💡 Usage

1. Open the Streamlit application.
2. Upload a PDF using the sidebar.
3. Click **Ingest Document**.
4. The backend extracts and chunks the document.
5. Document information is stored in FAISS.
6. Entities and relationships are stored in Neo4j.
7. Enter a question in the chat interface.
8. The system retrieves relevant information from FAISS and Neo4j.
9. The contexts are combined.
10. The LLM generates the final response.

## 🔄 End-to-End Flow

```text
             PDF Upload
                 ↓
          Streamlit Frontend
                 ↓
           FastAPI Backend
                 ↓
          Document Processing
                 ↓
          Text Chunking
                 ↓
        ┌────────┴─────────┐
        ↓                  ↓
     FAISS               Neo4j
 Vector Retrieval     Knowledge Graph
        ↓                  ↓
        └────────┬─────────┘
                 ↓
          Context Fusion
                 ↓
              LLM
                 ↓
          Final Response
                 ↓
          Streamlit UI
```

## 📁 Project Structure

```text
project/
│
├── frontend/
│   ├── app.py
│   └── ...
│
├── backend/
│   ├── ...
│   ├── .env.example
│   └── ...
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🔐 Security

* Store API keys in environment variables.
* Never commit `.env` files.
* Do not expose Neo4j credentials in source code.
* Use `.env.example` to document required configuration without storing secrets.

## 🛠️ Technologies

```text
Python
Streamlit
FastAPI
Uvicorn
LangChain
OpenAI
FAISS
Neo4j
Docker
Docker Compose
```

## 🎯 Project Goal

The goal of this project is to demonstrate how **Hybrid RAG** can combine:

* Semantic vector retrieval
* Knowledge graph reasoning
* LLM-based context fusion

to provide more context-aware responses from a document-based knowledge base.
