# Phase-Wise Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the step-by-step implementation plan for the Mutual Fund FAQ Assistant, based on the `docs/architecture.md` and project requirements.

---

## Phase 1: Environment Setup & Foundation
**Goal:** Initialize the project repository and set up the development environment.

*   **Step 1.1:** Initialize the Python environment (e.g., using `venv` or `conda`) with Python 3.10+.
*   **Step 1.2:** Define and install core dependencies (`requirements.txt`).
    *   Libraries: `langchain`, `llama-index` (if preferred), `chromadb`, `streamlit`, `beautifulsoup4`, `python-dotenv`, `groq`, and `sentence-transformers` (for BGE).
*   **Step 1.3:** Setup basic project structure (directories for `data`, `src`, `notebooks`, etc.).
*   **Step 1.4:** Securely manage API keys (LLM/Embeddings) using a `.env` file.

---

## Phase 2: Data Ingestion Module
**Goal:** Extract, clean, and chunk the data from the 5 predefined Navi mutual fund schemes on Groww.

*   **Step 2.1:** Develop a scraping script (using `BeautifulSoup` or similar) to fetch content from the 5 specific Groww URLs.
*   **Step 2.2:** Parse and clean the raw HTML, extracting meaningful text (factsheets, expense ratios, exit loads, etc.).
*   **Step 2.3:** Implement a Document-Level chunking strategy. Since the parsed fund facts are concise and dense key-value pairs, each fund's synthesized text block will be treated as a single, indivisible chunk to preserve context.
*   **Step 2.4:** Append origin metadata to every chunk (`source_url` and `last_updated_date`).

---

## Phase 3: Vector Database & Embedding
**Goal:** Convert text chunks into mathematical vectors and store them for similarity search.

*   **Step 3.1:** Initialize the embedding model (BGE model via HuggingFace).
*   **Step 3.2:** Generate embeddings for all the chunks created in Phase 2.
*   **Step 3.3:** Initialize a local Vector Database (e.g., `ChromaDB` or `FAISS`).
*   **Step 3.4:** Store the embeddings and their associated metadata in the Vector Database.
*   **Step 3.5:** Write a script to test Top-K similarity searches to ensure relevant chunks are successfully retrieved.

---

## Phase 4: Query Processing & Refusal Logic
**Goal:** Filter user inputs and reject advisory or non-factual queries.

*   **Step 4.1:** Develop the intent classification/refusal module.
    *   Use a lightweight prompt or predefined keywords to detect advisory queries like "Should I invest?" or "Which is better?".
*   **Step 4.2:** Implement the refusal response format (polite tone, reinforce "facts-only" rule, append an AMFI/SEBI educational link).
*   **Step 4.3:** Route factual queries directly to the vector database for embedding and similarity search.

---

## Phase 5: RAG Core & Generation Layer (LLM)
**Goal:** Formulate the final answers strictly based on retrieved context.

*   **Step 5.1:** Design the System Prompt.
    *   Enforce the "facts-only" and "no financial advice" persona.
    *   Strictly limit responses to the provided context.
    *   Instruct the LLM to reply with a maximum of **3 sentences**.
*   **Step 5.2:** Build the RAG chain connecting the user query, vector retrieval, and LLM generation.
    *   **Retrieval Strategy:** Use a Top-K similarity search with K=3. Since each chunk represents a complete fund profile (Document-Level chunking), retrieving the top 3 chunks provides comprehensive context for both specific and comparison queries while easily fitting in the LLM's context window.
*   **Step 5.3:** Implement the Response Formatter (Post-Processor).
    *   Extract the `source_url` from the retrieved context.
    *   Append exactly one citation link to the end of the LLM output.
    *   Append the footer: `"Last updated from sources: <date>"`.

---

## Phase 6: User Interface (UI) Development
**Goal:** Build a minimal, user-friendly frontend.

*   **Step 6.1:** Initialize a `Streamlit` application.
*   **Step 6.2:** Design the UI layout:
    *   Add a prominent welcome message.
    *   Display the mandatory disclaimer: *"Facts-only. No investment advice."*
    *   Include 3 clickable or visible example questions.
*   **Step 6.3:** Connect the Streamlit UI to the backend RAG pipeline.
*   **Step 6.4:** Ensure the chat interface gracefully handles refusals and displays formatted answers (with citations/footer).

---

## Phase 7: Testing, Validation & Documentation
**Goal:** Verify constraints are met and prepare the final deliverables.

*   **Step 7.1:** Conduct end-to-end testing with factual queries to ensure accurate retrieval and 3-sentence formatting.
*   **Step 7.2:** Stress-test the Refusal Module with edge-case advisory queries.
*   **Step 7.3:** Verify that no PII (session state) is being stored or tracked inappropriately.
*   **Step 7.4:** Draft the final `README.md` containing setup instructions, architecture overview, and known limitations.

---

## Phase 8: Data Ingestion Scheduler (GitHub Actions)
**Goal:** Automate the data ingestion pipeline to fetch the latest mutual fund data daily using a CI/CD workflow.

*   **Step 8.1:** Create a GitHub Actions workflow file (e.g., `.github/workflows/daily_ingestion.yml`).
*   **Step 8.2:** Configure a `schedule` trigger using cron syntax to run the workflow automatically once every day.
*   **Step 8.3:** Define the workflow steps to check out the repository, set up Python, install dependencies, and execute the full ingestion sequence (`scraper.py` -> `cleaner.py` -> `chunker.py` -> `vector_store.py`).
*   **Step 8.4:** Configure the workflow to commit and push the newly updated data files and vector database back to the `main` branch.
*   **Step 8.5:** Securely manage API keys (e.g., `GROQ_API_KEY`) by adding them to GitHub Actions Secrets and passing them to the workflow environment.
