import json
import os
from datetime import datetime
from langchain_core.documents import Document

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "cleaned_data.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "chunks.json")

def create_chunks():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    documents = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for item in data:
        # Step 2.3: Document-level chunking strategy
        # We take the pre-synthesized 'clean_text_for_rag' as a single, indivisible chunk per fund.
        text_content = item.get("clean_text_for_rag", "")
        
        # Step 2.4: Append origin metadata
        metadata = item.get("metadata", {})
        metadata["source_url"] = item.get("url", "")
        metadata["last_updated_date"] = current_date
        metadata["fund_name"] = item.get("name", "")
        
        # Create a LangChain Document object
        doc = Document(page_content=text_content, metadata=metadata)
        documents.append(doc)
        
    # Save the structured chunks to a JSON file for easy viewing and downstream use
    serialized_docs = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(serialized_docs, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully created {len(documents)} document-level chunks.")
    print(f"Saved chunks with origin metadata to {OUTPUT_FILE}")

if __name__ == "__main__":
    create_chunks()
