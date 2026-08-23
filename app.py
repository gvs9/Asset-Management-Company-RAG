import streamlit as st
from src.query_router import analyze_intent
from src.rag_pipeline import generate_answer

# Step 6.1 & 6.2: Initialize Streamlit and Design UI Layout
st.set_page_config(page_title="Navi Mutual Fund Assistant", page_icon="📈", layout="centered")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📈 Navi Mutual Fund FAQ Assistant")

# Display the mandatory disclaimer
st.warning("**Disclaimer:** Facts-only. No investment advice. This AI is strictly designed to provide factual information from official scheme documents. Please consult a financial advisor for investment decisions.")

st.markdown("Welcome! I am here to help you understand Navi Mutual Funds. Ask me factual questions about expense ratios, exit loads, fund managers, and more.")

# Include 3 visible example questions
with st.expander("💡 Click here for Example Questions", expanded=False):
    st.markdown("""
    Try asking:
    * *What is the expense ratio of the Navi Liquid Fund?*
    * *Who is the fund manager for the Hybrid fund?*
    * *What is the investment objective of the Nifty 50 Index Fund?*
    """)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Step 6.3 & 6.4: React to user input and connect backend ---
if prompt := st.chat_input("Ask a question about Navi Mutual Funds..."):
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Step 6.4: Guardrail check (Intent Classification)
    is_factual, refusal_response = analyze_intent(prompt)
    
    with st.chat_message("assistant"):
        if not is_factual:
            # Handle Refusals Gracefully
            st.error("Advisory Intent Detected")
            st.markdown(refusal_response)
            st.session_state.messages.append({"role": "assistant", "content": refusal_response})
        else:
            # Process via RAG Pipeline
            with st.spinner("Searching facts & generating response..."):
                answer = generate_answer(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
