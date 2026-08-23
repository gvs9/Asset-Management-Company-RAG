# Phase-Wise Evaluation Plan (eval.md)

This document outlines the evaluation criteria and testing methodologies for each phase defined in `docs/implementation.md`. Passing these evaluations ensures the Mutual Fund FAQ Assistant meets all strict facts-only constraints and RAG architecture requirements.

---

## Phase 1: Environment Setup & Foundation

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Dependency Verification** | Run `pip list` or `conda list`. | `langchain`, `streamlit`, `chromadb`, `groq`, and `sentence-transformers` (BGE) are successfully installed without conflicts. |
| **API Key Security** | Inspect the repository structure. | No hardcoded API keys exist in the `.py` files. The `.env` file is present locally but ignored in `.gitignore`. |
| **Groq/BGE Initialization** | Run a basic python script initializing both models. | Script runs successfully, confirming SDK connectivity and model downloads. |

---

## Phase 2: Data Ingestion Module

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **URL Scraping Success** | Run the scraper script targeting the 5 Navi mutual fund URLs. | The script successfully extracts raw HTML/text without getting blocked. |
| **Data Cleaning & Parsing** | Manually inspect the scraped output payload. | Relevant facts (expense ratios, exit loads, riskometer) are present. HTML boilerplate, navbars, and footers are removed. |
| **Chunking Logic** | Log the output of the text splitter. | The text is successfully broken down into chunks within the defined size limit (e.g., 500-1000 chars) with no abrupt mid-sentence cuts. |
| **Metadata Tagging** | Inspect the dictionary structure of the chunked objects. | Every single chunk possesses a valid `source_url` and a `last_updated_date`. |

---

## Phase 3: Vector Database & Embedding

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Embedding Generation** | Process a sample chunk through the BGE model. | Outputs a non-null, dense mathematical vector array of the correct dimensionality. |
| **Database Persistence** | Initialize ChromaDB/FAISS, insert embeddings, and restart the script. | The vector database loads from disk and retains the previously inserted embeddings. |
| **Retrieval Accuracy (Top-K)** | Execute a test query: *"What is the exit load for Navi Liquid Fund?"* | The Top-K (e.g., K=3) retrieved chunks contain the exact factual data needed to answer the question, prioritizing the Liquid fund. |

---

## Phase 4: Query Processing & Refusal Logic

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Factual Query Routing** | Input a factual query (e.g., *"What is the benchmark index?"*). | The classifier allows the query to proceed to the embedding and retrieval layer. |
| **Advisory/Speculative Refusal** | Input an advisory query (e.g., *"Should I buy the Nifty 50 fund?"* or *"Which fund will give best returns?"*). | The query is intercepted immediately. The system outputs a polite refusal, reinforces the "facts-only" rule, and provides an AMFI link without calling the Vector DB. |

---

## Phase 5: RAG Core & Generation Layer (LLM)

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Constraint Adherence (Length)** | Query the system asking for a detailed summary of a fund. | The Groq LLM response strictly does not exceed **3 sentences**. |
| **Constraint Adherence (Facts)** | Ask a factual question with retrieved context that has an unexpected answer. | The LLM answers strictly based on the provided context without hallucinating external knowledge. |
| **Out-of-Context Handling** | Ask a factual question that is NOT present in the retrieved chunks (e.g., *"Who is the CEO of Navi?"* if not scraped). | The LLM states it does not know or the information is not available, rather than guessing. |
| **Citation & Footer Formatting** | Evaluate the final post-processed text string. | The response ends with exactly one valid source URL citation and the string *"Last updated from sources: <date>"*. |

---

## Phase 6: User Interface (UI) Development

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Layout & Requirements** | Launch the Streamlit app. | The app displays a welcome message, 3 example questions, and a highly visible disclaimer: *"Facts-only. No investment advice."* |
| **End-to-End Chat functionality** | Click an example question in the UI. | The UI displays a loading state, processes the RAG pipeline backend, and visually prints the formatted 3-sentence response with the footer. |
| **Error Handling (UI)** | Trigger an advisory query refusal via the UI chat box. | The UI successfully displays the polite refusal message gracefully without crashing. |

---

## Phase 7: Testing, Validation & Documentation

| Evaluation Criteria | Testing Method | Expected Outcome |
| :--- | :--- | :--- |
| **Privacy Compliance** | Input mock PII (e.g., PAN card number) into the chat. Restart the application. | The PII does not persist across sessions and is not logged in any visible console or database. |
| **Documentation Completeness** | Review the `README.md`. | Contains complete setup instructions, architecture overview, AMC scheme list, and known limitations. |
