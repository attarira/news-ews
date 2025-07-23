# ingestion/newsdata_client.py

import os
import requests
import yaml
import json
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
NEWSDATA_KEY = os.getenv("NEWSDATA_KEY")

class NewsDataClient:
    def __init__(self, company_list_path: str = "data/company_list.yaml"):
        if not NEWSDATA_KEY:
            raise ValueError("NEWSDATA_KEY not found in environment variables")
        self.api_key = NEWSDATA_KEY
        self.base_url = "https://newsdata.io/api/1/news"
        self.load_company_list(company_list_path)

    def load_company_list(self, path):
        with open(path, "r") as file:
            data = yaml.safe_load(file)
            self.companies = data["companies"]

    def fetch_articles_for_company(self, company):
        query = " OR ".join([alias for alias in company["aliases"]])
        params = {
            "apikey": self.api_key,
            "q": query,
            "language": "en",
            "page": 1
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            print(f"[NewsData] Error fetching for {company['name']}: {response.text}")
            return []

    def save_articles(self, company_name, articles):
        if not articles:
            return
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = "data/raw"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{company_name.replace(' ', '_')}_{date_str}_newsdata.json"
        with open(filename, "w") as f:
            json.dump(articles, f, indent=2)
        print(f"[NewsData] Saved {len(articles)} articles for {company_name} to {filename}")