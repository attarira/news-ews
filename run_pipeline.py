# run_pipeline.py

from ingestion.fetcher import NewsFetcher

if __name__ == "__main__":
    fetcher = NewsFetcher()
    fetcher.fetch_all()