import feedparser
import boto3
import json

# Configurations
RSS_FEED_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"
AWS_REGION = "eu-central-1"
KEYWORDS = ["Trump"]

# Initialize Amazon Comprehend client
comprehend = boto3.client(
    'comprehend',
    region_name=AWS_REGION,
)


def fetch_and_filter_feed(feed_url, keywords):
    feed = feedparser.parse(feed_url)
    print(f"Fetched {len(feed.entries)} entries from {feed.feed.title}")
    filtered_entries = []
    for entry in feed.entries:
        for keyword in keywords:
            if keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower():
                filtered_entries.append(entry)
                break
    print(f"Filtered {len(filtered_entries)} entries with keywords: {keywords}")
    return filtered_entries


def analyze_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']





def recognize_entities(text):
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    return response['Entities']


def extract_key_phrases(text):
    response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    return response['KeyPhrases']


def generate_alert(entry, sentiment, entities, key_phrases):
    alert = {
        "title": entry.title,
        "summary": entry.summary,
        "link": entry.link,
        "sentiment": sentiment,
        "entities": [f'{entity["Type"]}: {entity["Text"]}' for entity in entities],
        "key_phrases": [key_phrase["Text"] for key_phrase in key_phrases],
    }
    print(f"Alert generated: {json.dumps(alert, indent=2)}\n")


def process_entries(entries):
    for entry in entries:
        print(f"Processing entry: {entry.title}")
        text = entry.title + " " + entry.summary

        sentiment = analyze_sentiment(text)

        if sentiment == 'NEGATIVE':
            entities = recognize_entities(text)
            key_phrases = extract_key_phrases(text)

            generate_alert(entry, sentiment, entities, key_phrases)
        else:
            print(f"Sentiment is not negative: {sentiment}, skipping alert generation\n")


if __name__ == "__main__":
    entries = fetch_and_filter_feed(RSS_FEED_URL, KEYWORDS)
    process_entries(entries)
