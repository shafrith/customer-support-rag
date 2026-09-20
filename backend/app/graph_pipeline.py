import os
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

def create_and_store_knowledge_graph(chunks):
    """Extracts entities and stores them in Neo4j."""
    print("Connecting to Neo4j...")
    
    # Pulls all credentials, including the empty database variable, from .env
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=os.getenv("NEO4J_DATABASE") or None 
    )
    
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    print("Extracting entities and relationships (this may take a moment)...")
    transformer = LLMGraphTransformer(llm=llm)
    graph_documents = transformer.convert_to_graph_documents(chunks)
    
    print("Storing relationships into Neo4j database...")
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )
    print("Knowledge Graph built successfully!")
    return graph

def get_graph_connection():
    """Returns an active connection to the Neo4j database."""
    return Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=os.getenv("NEO4J_DATABASE") or None
    )