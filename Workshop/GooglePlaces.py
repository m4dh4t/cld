import requests
import json

import boto3

API_KEY = "<YOUR_API_KEY>"
AWS_REGION = "eu-central-1"

PLACES = [
    "Restaurant Au Sapin, Givrins",
    "Gymnase de Nyon"
]

COMPREHEND = boto3.client(
    'comprehend',
    region_name=AWS_REGION,
)


def fetch_place(place):
    r = requests.post(
        "https://places.googleapis.com/v1/places:searchText",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "places.id,places.displayName.text,places.displayName.languageCode"
        },
        data=json.dumps({
            "textQuery": place
        })
    )
    if r.status_code != 200:
        raise Exception(f"Error: {r.content}")

    places = json.loads(r.text)["places"]

    print(f"Found {len(places)} places, using most relevant one...")
    id = places[0]["id"]
    name = places[0]["displayName"]["text"]
    language = places[0]["displayName"]["languageCode"]

    return id, name, language


def fetch_place_reviews(id, language):
    r = requests.get(
        f"https://places.googleapis.com/v1/places/{id}",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "reviews",
        },
        params={
            "languageCode": language
        }
    )
    if r.status_code != 200:
        raise Exception(f"Error: {r.content}")

    reviews = json.loads(r.text)["reviews"]

    return reviews


if __name__ == "__main__":
    for place in PLACES:
        print(f"Looking up {place}...")
        id, name, language = fetch_place(place)

        print(f"Fetching reviews for {name}...")
        reviews = fetch_place_reviews(id, language)

        for review in reviews:
            print(f"Review date: {review['relativePublishTimeDescription']}, language: {review['originalText']['languageCode']}")
            sentiment = COMPREHEND.detect_sentiment(
                Text=review["originalText"]["text"],
                LanguageCode=review["originalText"]["languageCode"].split("-")[0]
            )["Sentiment"]

            if sentiment == "NEGATIVE":
                print(f"Sentiment: {sentiment}, ALERT: {review['originalText']['text']}\n")
            else:
                print(f"Sentiment: {sentiment}, skipping...\n")
