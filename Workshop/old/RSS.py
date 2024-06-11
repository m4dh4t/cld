import feedparser
import newspaper
import boto3
import json

# Configurations
AWS_REGION = "eu-central-1"

RSS_GNEWS_URL = "https://news.google.com/rss"
RSS_GNEWS_SEARCH_URL = f"{RSS_GNEWS_URL}/search?q="

KEYWORDS = ["Gaza"]
LANGUAGES = ["US:en", "FR:fr", "DE:de"]
MAX_ARTICLES = 10
MAX_TEXT_SIZE = 5000

# Initialize Amazon Comprehend client
comprehend = boto3.client(
    'comprehend',
    region_name=AWS_REGION,
)


def fetch_keyword_feed(keyword, language):
    print(f"Fetching feed for keyword: {keyword}...")
    feed = feedparser.parse(f"{RSS_GNEWS_SEARCH_URL}{keyword}&ceid={language}")
    entries = feed.entries[:MAX_ARTICLES]
    print(f"Fetched {len(entries)} entries\n")

    return entries


def generate_alert(entry, sentiment, entities, key_phrases):
    alert = {
        "title": entry.title,
        "link": entry.link,
        "sentiment": sentiment,
        "entities": [f'{entity["Type"]}: {entity["Text"]}' for entity in entities],
        "key_phrases": [key_phrase["Text"] for key_phrase in key_phrases],
    }
    print(f"Alert generated: {json.dumps(alert, indent=2)}\n")


def process_entries(entries, language):
    language_code = language.split(":")[1]

    for entry in entries:
        print(f"Processing entry: {entry.title}")
        article = newspaper.Article(entry.link)
        article.download()

        try:
            article.parse()
        except newspaper.article.ArticleException as e:
            print(f"Error: {e}, skipping...\n")
            continue

        # Limit text size to avoid Comprehend API limits
        text = article.text.encode('utf-8')[:MAX_TEXT_SIZE].decode('utf-8', 'ignore')

        print(f"Analyzing sentiment for: {entry.title}")
        sentiment = comprehend.detect_sentiment(Text=entry.title, LanguageCode=language_code)['Sentiment']
        if sentiment == 'NEGATIVE':
            print(f"ALERT: {entry.title}\n")

            # TODO: Remove early return to process entities and key phrases
            return
            entities = comprehend.detect_entities(Text=text, LanguageCode=language_code)['Entities']
            key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)['KeyPhrases']

            generate_alert(entry, text, sentiment, entities, key_phrases)
        else:
            print(f"Sentiment: {sentiment}")
            print("Skipping...\n")


if __name__ == "__main__":
    for keyword in KEYWORDS:
        print(f"Processing keyword: {keyword}")

        for language in LANGUAGES:
            print(f"Processing language: {language}")

            entries = fetch_keyword_feed(keyword, language)
            process_entries(entries, language)
            break
