import os
import requests
from bs4 import BeautifulSoup
import json
import time

URLS = [
    "https://groww.in/mutual-funds/navi-nifty-50-index-fund-direct-growth",
    "https://groww.in/mutual-funds/navi-nifty-midsmallcap-400-index-fund-direct-growth",
    "https://groww.in/mutual-funds/navi-liquid-fund-direct-growth",
    "https://groww.in/mutual-funds/navi-aggressive-hybrid-fund-direct-growth",
    "https://groww.in/mutual-funds/navi-nifty-500-multicap-50:25:25-index-fund-direct-growth"
]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def scrape_urls(urls):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    scraped_data = []

    for url in urls:
        print(f"Scraping: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements to clean the text
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text and clean it up
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up excessive whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            scraped_data.append({
                "url": url,
                "raw_text": clean_text
            })
            
            print(f"Successfully scraped {len(clean_text)} characters.")
            
        except requests.RequestException as e:
            print(f"Failed to scrape {url}: {e}")
            
        time.sleep(2) # Be polite and avoid rate limits

    # Save to JSON
    output_file = os.path.join(DATA_DIR, "scraped_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    scrape_urls(URLS)
