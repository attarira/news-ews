import os
import json
import time
from newspaper import Article

# Test input file (adjust if needed)
RAW_ARTICLES_PATH = "../data/raw/tesla_newsapi.json"
OUTPUT_PATH = "../data/full/tesla_newsapi_test.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def fetch_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"[Error] Failed to fetch article: {url}\n{e}")
        return None

if __name__ == "__main__":
    # Load just the first article
    with open(RAW_ARTICLES_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("No articles found in input.")
        exit(1)

    first_article = articles[0]
    url = first_article.get("url")
    print(f"Fetching full text for: {url}")

    full_text = fetch_full_text(url)
    first_article["full_text"] = full_text

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(first_article, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved enriched article to {OUTPUT_PATH}")