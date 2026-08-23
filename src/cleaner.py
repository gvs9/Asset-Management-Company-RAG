import json
import re
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "scraped_data.json")
OUTPUT_MD = os.path.join(DATA_DIR, "review.md")
OUTPUT_JSON = os.path.join(DATA_DIR, "cleaned_data.json")

def extract_metric(text, pattern, group=1):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(group).strip()
    return "Not found"

def clean_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_records = []
    
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Mutual Funds Data Review\n\n")
        f.write("Here is the parsed and cleaned data extracted from the scraped URLs for your review:\n\n")
        
        for item in data:
            url = item.get("url", "")
            raw_text = item.get("raw_text", "")
            
            # Extract key fields
            name_match = re.search(r"Navi.*?Fund", raw_text)
            name = name_match.group(0) if name_match else url.split("/")[-1]
            
            expense_ratio = extract_metric(raw_text, r"Expense ratio\s+([0-9.]+%?)")
            exit_load = extract_metric(raw_text, r"Exit load\s+(.*?)\s+Stamp duty")
            min_sip = extract_metric(raw_text, r"Min\. for SIP\s+(₹[0-9,]+)")
            aum = extract_metric(raw_text, r"Fund size \(AUM\)\s+(₹[0-9,.]+\s+Cr)")
            
            risk_match = re.search(r"(Very High Risk|High Risk|Moderately High Risk|Moderate Risk|Low to Moderate Risk|Low Risk)", raw_text, re.IGNORECASE)
            risk = risk_match.group(1).strip() if risk_match else "Not found"
            
            objective = extract_metric(raw_text, r"Investment Objective\s+(.*?)(?:Fund benchmark|Scheme Information Document)", 1)
            
            manager = "Not found"
            manager_match = re.search(r"Fund management\s+[A-Z]{2,3}\s+([A-Za-z\s]+)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", raw_text)
            if manager_match:
                manager = manager_match.group(1).strip()
            
            # Construct a clean text document intended for RAG
            clean_text_for_rag = (
                f"Fund Name: {name}\n"
                f"Fund URL: {url}\n"
                f"Expense Ratio: {expense_ratio}\n"
                f"Exit Load: {exit_load}\n"
                f"Minimum SIP Amount: {min_sip}\n"
                f"Fund Size (AUM): {aum}\n"
                f"Riskometer Classification: {risk}\n"
                f"Investment Objective: {objective}\n"
                f"Fund Manager: {manager}\n"
            )
            
            cleaned_records.append({
                "url": url,
                "name": name,
                "clean_text_for_rag": clean_text_for_rag,
                "metadata": {
                    "expense_ratio": expense_ratio,
                    "exit_load": exit_load,
                    "min_sip": min_sip,
                    "aum": aum,
                    "risk": risk
                }
            })
            
            f.write(f"## {name}\n")
            f.write(f"- **URL:** {url}\n")
            f.write(f"- **Expense Ratio:** {expense_ratio}\n")
            f.write(f"- **Exit Load:** {exit_load}\n")
            f.write(f"- **Minimum SIP:** {min_sip}\n")
            f.write(f"- **Fund Size (AUM):** {aum}\n")
            f.write(f"- **Riskometer:** {risk}\n")
            f.write(f"- **Investment Objective:** {objective}\n")
            f.write(f"- **Fund Manager:** {manager}\n")
            f.write("\n---\n\n")
            
    # Save the JSON representation for the chunking pipeline (Step 2.3)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(cleaned_records, f, ensure_ascii=False, indent=4)
        
    print(f"Markdown review written to {OUTPUT_MD}")
    print(f"Cleaned JSON for RAG pipeline written to {OUTPUT_JSON}")

if __name__ == "__main__":
    clean_data()
