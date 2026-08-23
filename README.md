# Navi Mutual Fund FAQ Assistant

An AI-powered factual assistant designed to answer questions about 5 specific Navi Mutual Fund schemes based exclusively on official data from Groww. It ensures that responses are restricted strictly to factual information and actively refuses any queries seeking financial advice, recommendations, or predictions.

## Architecture Overview

The system is built on a standard Retrieval-Augmented Generation (RAG) pipeline:
- **Data Ingestion**: Scrapes 5 Navi Mutual Fund scheme URLs on Groww, extracting raw HTML.
- **Chunking**: Uses Document-Level chunking to keep each fund's extracted key-value parameters cohesive.
- **Vector Database**: Embeds chunks using the `BAAI/bge-small-en-v1.5` model and stores them in ChromaDB.
- **Query Router / Refusal Module**: Uses Regex pattern matching to intercept and reject advisory queries before they reach the LLM.
- **LLM Generation**: Uses Groq API (Qwen model) with a strict system prompt (max 3 sentences) to answer based purely on retrieved context.
- **UI**: A minimal, user-friendly frontend built with Streamlit.

## Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory.
2. **Set up a Python Virtual Environment** (Python 3.10+ recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL_NAME=qwen/qwen3.6-27b
   ```
5. **Data Setup** (If you haven't run the ingestion pipeline yet):
   ```bash
   python src/scraper.py
   python src/cleaner.py
   python src/chunker.py
   python src/vector_store.py
   ```
6. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Known Limitations

- **Strict Factual Enforcement**: The assistant may refuse legitimate questions if they trigger the advisory keywords (e.g., using words like "best" or "recommend").
- **Static Knowledge**: The application currently relies on a static snapshot of scraped data. It does not auto-update real-time NAV or fund parameters unless the ingestion scripts are re-run.
- **Rate Limits**: Subject to free-tier API rate limits from Groq if the application experiences high usage. Retries are implemented but some wait time might occur.

## Data Privacy & PII
- The application does not collect, store, or transmit any Personally Identifiable Information (PII).
- Session state is strictly limited to the temporary chat history (prompts and answers) for the duration of the browser session.
