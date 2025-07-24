import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

INPUT_DIR = "../data/full"
OUTPUT_DIR = "../data/sentiment"

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the first JSON file in data/full
def get_first_article_path():
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".json"):
            return os.path.join(INPUT_DIR, fname)
    return None

def load_article(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)

def main():
    article_path = get_first_article_path()
    if not article_path:
        print("No article found in data/full/")
        return

    article = load_article(article_path)
    full_text = article.get("full_text", "")

    if not full_text:
        print(f"No 'full_text' found in {article_path}")
        return

    sentiment = analyze_sentiment(full_text)

    print(f"\n📄 Title: {article.get('title')}")
    print(f"🌐 Source: {article.get('source', {}).get('name')}")
    print(f"🔗 URL: {article.get('url')}")
    print(f"\n🧠 Sentiment Scores: {sentiment}")

    # Save results
    result = {
        "title": article.get("title"),
        "url": article.get("url"),
        "source": article.get("source"),
        "sentiment": sentiment
    }

    out_fname = os.path.basename(article_path)
    out_path = os.path.join(OUTPUT_DIR, out_fname)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Sentiment saved to: {out_path}")

if __name__ == "__main__":
    main()