# ingestion/newsapi_client.py

import os
import requests
import yaml
from datetime import datetime
import json

class NewsAPIClient:
    def __init__(self, api_key: str, company_list_path: str = "data/company_list.yaml"):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
        self.load_company_list(company_list_path)

    def load_company_list(self, path):
        with open(path, "r") as file:
            data = yaml.safe_load(file)
            self.companies = data["companies"]

    def fetch_articles_for_company(self, company):
        """
        Fetch news articles for a single company
        """
        query = " OR ".join([f'"{alias}"' for alias in company["aliases"]])
        params = {
            "q": query,
            "language": "en",  # Start with English for demo
            "sortBy": "publishedAt",
            "pageSize": 50,
            "apiKey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()["articles"]
        else:
            print(f"Error fetching for {company['name']}: {response.text}")
            return []

    def save_articles(self, company_name, articles):
        """
        Save fetched articles to data/raw/company_name_DATE.json
        """
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = "data/raw"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{company_name.replace(' ', '_')}_{date_str}.json"
        with open(filename, "w") as f:
            json.dump(articles, f, indent=2)
        print(f"Saved {len(articles)} articles for {company_name} to {filename}")

    def fetch_and_save_all(self):
        """
        Fetch and save articles for all companies
        """
        for company in self.companies:
            print(f"Fetching articles for: {company['name']}")
            articles = self.fetch_articles_for_company(company)
            if articles:
                self.save_articles(company["name"], articles)