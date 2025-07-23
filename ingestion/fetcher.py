# ingestion/fetcher.py

from ingestion.newsapi_client import NewsAPIClient
from ingestion.newsdata_client import NewsDataClient

class NewsFetcher:
    def __init__(self):
        self.newsapi = NewsAPIClient()
        self.newsdata = NewsDataClient()

    def fetch_all(self):
        """
        Fetch and save articles from both APIs for all companies
        """
        for company in self.newsapi.companies:
            print(f"Fetching articles for {company['name']}...")
            # Try NewsAPI first
            articles = self.newsapi.fetch_articles_for_company(company)
            if articles:
                self.newsapi.save_articles(company["name"], articles)
            else:
                print(f"[Fallback] Trying NewsData.io for {company['name']}...")
                articles = self.newsdata.fetch_articles_for_company(company)
                if articles:
                    self.newsdata.save_articles(company["name"], articles)
                else:
                    print(f"[Warning] No articles found for {company['name']} in either API.")