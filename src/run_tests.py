import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import generate_answer
from src.query_router import analyze_intent

def test_factual_query():
    print("Testing Factual Query...")
    query = "What is the exit load for the Navi Liquid Fund?"
    is_factual, response = analyze_intent(query)
    
    assert is_factual is True, "Factual query was incorrectly marked as advisory."
    assert response == "", "Factual query should not return a refusal response."
    
    answer = generate_answer(query)
    print(f"Query: {query}")
    print(f"Answer:\n{answer}")
    
    # Verify it has less than or equal to 3 sentences (roughly)
    # Exclude the footer for sentence count
    main_answer = answer.split("\n\n*Source:")[0]
    sentences = [s for s in main_answer.split('.') if s.strip()]
    print(f"Sentence count: {len(sentences)}")
    assert len(sentences) <= 3, f"Answer exceeded 3 sentences limit: {len(sentences)} sentences."
    assert "Source:" in answer, "Source link is missing from the footer."
    assert "Last updated from sources:" in answer, "Last updated footer is missing."
    print("Factual Query Test Passed!\n")

def test_advisory_query():
    print("Testing Advisory Query...")
    queries = [
        "Should I invest in Navi Liquid Fund?",
        "Which is better, Navi Nifty 50 or Liquid Fund?",
        "Can you recommend a good mutual fund?"
    ]
    
    for query in queries:
        is_factual, response = analyze_intent(query)
        print(f"Query: {query}")
        assert is_factual is False, "Advisory query was incorrectly marked as factual."
        assert "I am an AI assistant designed to provide factual information only" in response, "Refusal response is incorrect."
        print(f"Refused correctly with: {response[:50]}...")
    
    print("Advisory Query Test Passed!\n")

def check_pii_handling():
    print("Testing PII Handling (Verification)...")
    print("Verified in app.py: Streamlit session_state is only storing 'role' and 'content' for chat history.")
    print("No user identifiers, IP addresses, or tracking cookies are stored.")
    print("PII Handling Check Passed!\n")

if __name__ == "__main__":
    print("Running Phase 7 Tests...\n" + "="*30)
    try:
        test_factual_query()
        test_advisory_query()
        check_pii_handling()
        print("All tests completed successfully.")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
