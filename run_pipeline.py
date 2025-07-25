# run_pipeline.py


import os
import glob
import json
from ingestion.fetcher import NewsFetcher
from processing.absa import analyze_aspect_sentiment


def get_company_article_files(raw_data_dir="data/raw"):
    """Return list of all JSON files with raw articles."""
    return glob.glob(os.path.join(raw_data_dir, "*.json"))

def load_articles_from_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def run_absa_on_articles(articles, company_name):
    print(f"\n=== Running ABSA for company: {company_name} ===")
    for idx, article in enumerate(articles):
        text = article.get("content") or article.get("description") or article.get("title")
        if not text:
            continue
        print(f"\nArticle #{idx+1}: {article.get('title', '')}")
        absa_result = analyze_aspect_sentiment(text, target_entity=company_name)
        print(f"Result: {absa_result}\n")

if __name__ == "__main__":
    # Step 1: Fetch articles
    fetcher = NewsFetcher()
    fetcher.fetch_all()

    # Step 2: For each company, load articles and run ABSA
    article_files = get_company_article_files()
    for file_path in article_files:
        company_name = os.path.splitext(os.path.basename(file_path))[0].replace('_newsapi', '').replace('_newsdata', '')
        articles = load_articles_from_file(file_path)
        run_absa_on_articles(articles, company_name)