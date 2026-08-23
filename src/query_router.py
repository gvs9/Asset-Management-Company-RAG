import re
from typing import Tuple

# Step 4.2: The standard refusal response
REFUSAL_RESPONSE = (
    "I am an AI assistant designed to provide factual information only. "
    "I cannot offer financial advice, recommend funds, or predict market performance. "
    "For guidance on investing, please consult a certified financial advisor or visit the "
    "[AMFI Investor Corner](https://www.amfiindia.com/investor-corner) for educational resources."
)

# Step 4.1: Predefined keywords and regex patterns to detect advisory intent
ADVISORY_PATTERNS = [
    r"\b(should|where|how)\s+(i|we)\s+invest\b",
    r"\bwhich\s+(fund\s+)?is\s+better\b",
    r"\bbest\s+(mutual\s+)?fund\b",
    r"\b(recommend|suggest|advise)\b",
    r"\bgood\s+investment\b",
    r"\bwill\s+(it|the\s+fund)\s+(go\s+up|go\s+down|increase|decrease)\b",
    r"\bpredict\b",
    r"\bmy\s+portfolio\b",
    r"\bfinancial\s+advice\b",
    r"\bis\s+this\s+a\s+good\s+time\s+to\s+invest\b"
]

def analyze_intent(query: str) -> Tuple[bool, str]:
    """
    Step 4.1 & 4.3: Intent classification module.
    Returns a tuple: (is_factual, response)
    - If is_factual is True, response is empty string -> Route to Vector DB (RAG).
    - If is_factual is False, response contains the formatted refusal message.
    """
    query_lower = query.lower()
    
    for pattern in ADVISORY_PATTERNS:
        if re.search(pattern, query_lower):
            # Intent is advisory, reject the query
            return False, REFUSAL_RESPONSE
            
    # Intent is factual, proceed to RAG
    return True, ""

if __name__ == "__main__":
    # Edge-case testing to ensure accuracy
    test_queries = [
        "What is the expense ratio of the Navi Liquid Fund?",
        "Should I invest my life savings in the Nifty 50 fund?",
        "Which fund is better, Nifty 50 or Liquid fund?",
        "Who is the fund manager for the Hybrid fund?",
        "Can you recommend a good mutual fund for a 5 year horizon?",
        "What is the exit load for the midcap fund?"
    ]
    
    print("Testing Query Router / Refusal Logic:\n")
    for q in test_queries:
        is_factual, response = analyze_intent(q)
        print(f"Query: '{q}'")
        if is_factual:
            print("Action: [PROCEED TO RAG] (Factual query)")
        else:
            print(f"Action: [REJECT] (Advisory query)\nResponse: {response}")
        print("-" * 60)
