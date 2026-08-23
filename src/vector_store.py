import os
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHUNKS_FILE = os.path.join(DATA_DIR, "chunks.json")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")

def get_embedding_model():
    """Step 3.1: Initialize the BGE embedding model."""
    print("Initializing BGE Embedding Model...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True} 
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings

def build_vector_store():
    """Steps 3.2, 3.3, 3.4: Generate embeddings and store in ChromaDB."""
    if not os.path.exists(CHUNKS_FILE):
        print(f"Error: {CHUNKS_FILE} not found.")
        return None

    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)

    # Reconstruct LangChain Document objects
    documents = [
        Document(page_content=item["page_content"], metadata=item["metadata"])
        for item in chunk_data
    ]
    
    print(f"Loaded {len(documents)} documents for embedding.")
    
    embedder = get_embedding_model()
    
    print("Initializing ChromaDB and storing embeddings...")
    # Initialize ChromaDB and add documents
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedder,
        persist_directory=CHROMA_DB_DIR
    )
    
    print(f"Successfully stored {len(documents)} embeddings in Vector Database at {CHROMA_DB_DIR}")
    return vector_store

def test_retrieval(query: str, k: int = 2):
    """Step 3.5: Test Top-K similarity search."""
    print(f"\n--- Testing Retrieval for Query: '{query}' ---")
    embedder = get_embedding_model()
    
    # Load existing DB
    vector_store = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedder)
    
    results = vector_store.similarity_search_with_score(query, k=k)
    
    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i+1} (Score: {score:.4f}):")
        print(f"Fund Name: {doc.metadata.get('fund_name')}")
        print(f"Content snippet: {doc.page_content[:150]}...")
        
    return results

if __name__ == "__main__":
    # Execute full pipeline (Steps 3.2, 3.3, 3.4)
    build_vector_store()
    
    # Test retrieval (Step 3.5)
    test_retrieval("Which fund has the lowest expense ratio?")
    test_retrieval("What is the risk level for the Liquid Fund?")
