from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Updated Import Path
from langchain_neo4j import GraphCypherQAChain

from app.vector_pipeline import load_vector_store
from app.graph_pipeline import get_graph_connection

def generate_hybrid_response(query: str) -> str:
    """Combines FAISS semantic search and Neo4j relational search."""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    # 1. Vector Retrieval
    print("Searching Vector Database...")
    vector_store = load_vector_store()
    vector_docs = vector_store.similarity_search(query, k=3)
    vector_context = "\n".join([doc.page_content for doc in vector_docs])
    
    # 2. Graph Retrieval
    print("Searching Knowledge Graph...")
    graph = get_graph_connection()
    graph_chain = GraphCypherQAChain.from_llm(
        llm=llm, 
        graph=graph, 
        verbose=True,
        return_direct=True,
        allow_dangerous_requests=True # Required by newer LangChain versions
    )
    
    try:
        graph_response = graph_chain.invoke({"query": query})
        graph_context = graph_response.get("result", "No relational data found.")
    except Exception as e:
        print(f"Graph query failed: {e}")
        graph_context = "No relational data found."

    # 3. Fusion Prompt
    print("Fusing contexts and generating final response...")
    prompt_template = """
    You are an expert customer support agent. Answer the user's question using ONLY the context provided below. 
    Combine insights from both the document text and the entity relationships to form a complete answer.
    If the answer is not contained in the context, say "I don't have enough information to answer that."

    --- Semantic Context (From Documents) ---
    {vector_context}
    
    --- Relational Context (From Knowledge Graph) ---
    {graph_context}
    
    User Question: {query}
    
    Helpful Answer:"""
    
    prompt = PromptTemplate.from_template(prompt_template)
    generation_chain = prompt | llm | StrOutputParser()
    
    final_answer = generation_chain.invoke({
        "vector_context": vector_context,
        "graph_context": graph_context,
        "query": query
    })
    
    return final_answer