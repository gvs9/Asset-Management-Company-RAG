import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
from dotenv import load_dotenv
from groq import Groq
from src.vector_store import get_embedding_model
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "qwen/qwen3.6-27b")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")

# Initialize the Groq client securely. Fallback to None if key is missing so the app doesn't crash on import.
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def get_retriever():
    """Initializes the Vector DB retriever with Top-K=3 strategy."""
    embedder = get_embedding_model()
    vector_store = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedder)
    
    # Retrieval Strategy: Top-K=3 as defined in Phase 5
    return vector_store.as_retriever(search_kwargs={"k": 3})

def generate_answer(query: str) -> str:
    """
    Step 5.2: Build the RAG chain and generate the answer.
    """
    if client is None:
        return "Server Configuration Error: The GROQ_API_KEY environment variable has not been set in Railway."
    retriever = get_retriever()
    retrieved_docs = retriever.invoke(query)
    
    if not retrieved_docs:
        return "I could not find any relevant factual information to answer your query."

    # Construct the context block
    context_parts = []
    source_url = None
    last_updated = None
    
    for doc in retrieved_docs:
        context_parts.append(doc.page_content)
        # Grab metadata from the top most relevant document
        if source_url is None:
            source_url = doc.metadata.get("source_url")
            last_updated = doc.metadata.get("last_updated_date")
            
    context_text = "\n\n---\n\n".join(context_parts)
    
    # Step 5.1: Design the System Prompt
    system_prompt = (
        "You are a strict, factual Mutual Fund assistant. "
        "Strictly limit your response to a maximum of 3 sentences. "
        "Only answer based on the provided context. Do NOT provide financial advice.\n"
        "Provide your final answer immediately. Do NOT output any <think> blocks, reasoning, or internal thoughts."
    )
    
    user_prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
    
    # Step 5.2: Groq API Call with strict limits to handle TPM and RPM limits
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=GROQ_MODEL_NAME,
                max_tokens=512,  # Increased cap to allow Qwen to complete its <think> process
                temperature=0.0  # Zero temperature for facts-only retrieval
            )
            raw_answer = response.choices[0].message.content.strip()
            
            # Remove <think>...</think> blocks from Qwen's output
            if "</think>" in raw_answer:
                answer = raw_answer.split("</think>")[-1].strip()
            else:
                # If there is no closing tag, it might be purely an answer or cut off.
                answer = re.sub(r'<think>.*', '', raw_answer, flags=re.DOTALL).strip()
                if not answer:
                    answer = raw_answer.strip()
            
            # Step 5.3: Implement the Response Formatter (Append metadata)
            if source_url:
                footer = f"\n\n*Source: {source_url}*\n*Last updated from sources: {last_updated}*"
                return answer + footer
            return answer
            
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                print(f"Rate limit reached. Retrying in 5 seconds (Attempt {attempt+1}/{max_retries})...")
                time.sleep(5)
            else:
                return f"An error occurred while generating the response: {e}"

if __name__ == "__main__":
    # Test the RAG pipeline
    print(f"Testing RAG Pipeline using Groq model: {GROQ_MODEL_NAME}...\n")
    test_query = "What is the exit load and expense ratio for the Navi Liquid Fund?"
    print(f"Query: {test_query}\n")
    print(generate_answer(test_query))
