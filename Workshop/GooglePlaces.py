import os
import json
import boto3
import urllib3

GPLACES_API_URL = "https://places.googleapis.com/v1/places"
GPLACES_API_KEY = os.environ["GPLACES_API"]

COMPREHEND = boto3.client("comprehend")

S3 = boto3.client("s3")
S3_BUCKET = "cld-workshopteam9"

GLUE = boto3.client("glue")
GLUE_CRAWLER = "cld-workshopteam9-comprehend-analysis-crawler"

http = urllib3.PoolManager()


def fetch_place(place):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GPLACES_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName.text,places.displayName.languageCode"
    }
    body = json.dumps({
        "textQuery": place
    })
    r = http.request(
        "POST",
        f"{GPLACES_API_URL}:searchText",
        headers=headers,
        body=body
    )
    
    if r.status != 200:
        raise Exception(f"Error: {r.data.decode('utf-8')}")

    places = json.loads(r.data.decode('utf-8'))["places"]

    print(f"Found {len(places)} places, using most relevant one...")
    id = places[0]["id"]
    name = places[0]["displayName"]["text"]

    return id, name


def fetch_place_reviews(id):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GPLACES_API_KEY,
        "X-Goog-FieldMask": "reviews",
    }
    r = http.request(
        "GET",
        f"{GPLACES_API_URL}/{id}",
        headers=headers,
    )

    if r.status != 200:
        raise Exception(f"Error: {r.data.decode('utf-8')}")

    reviews = json.loads(r.data.decode('utf-8'))["reviews"]

    return reviews


def clean_s3_folder(bucket, folder):
    try:
        response = S3.list_objects_v2(Bucket=bucket, Prefix=folder)
        if "Contents" in response:
            objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"] if obj["Key"] != folder]
            S3.delete_objects(Bucket=bucket, Delete={"Objects": objects_to_delete})
            print(f"Deleted {len(objects_to_delete)} objects from {folder}")
        else:
            print(f"No objects found in {folder}")
    except Exception as e:
        print(f"Error cleaning S3 folder {folder}: {str(e)}")


def upload_to_s3(data, filename):
    try:
        S3.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=json.dumps(data)
        )
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")


def lambda_handler(event, context):
    # Clean S3 folders at the start of the Lambda function
    folders = {
        "sentiment": "sentiment-results/",
        "entities": "entities-results/",
        "targeted_sentiment": "targeted-sentiment-results/"
    }
    for folder in folders.values():
        clean_s3_folder(S3_BUCKET, folder)


    # Get places from event
    places = event.get("places", [])
    if not places:
        return {
            "statusCode": 400,
            "body": "No places provided."
        }


    # Iterate on all given places
    for place in places:
        print(f"Looking up {place}...")
        id, name = fetch_place(place)

        print(f"Fetching reviews for {name}...")
        reviews = fetch_place_reviews(id)

        for i, review in enumerate(reviews):
            print(f"Review date: {review['relativePublishTimeDescription']}, language: {review['originalText']['languageCode']}")
            review_text = review["text"]["text"]


            # Detect sentiment
            sentiment = COMPREHEND.detect_sentiment(
                Text=review_text,
                LanguageCode="en",
            )
            upload_to_s3(
                {
                    "name": name,
                    "sentiment": sentiment["Sentiment"]
                },
                f"{folders['sentiment']}{name}_review{i}"
            )
            print(f"{name}({i}): Sentiment analysis uploaded to S3 ({S3_BUCKET})")


            # Detect entities
            entities = COMPREHEND.detect_entities(
                Text=review_text,
                LanguageCode="en",
            )
            for entity in entities["Entities"]:
                upload_to_s3(
                    {
                        "name": name,
                        "entity": entity["Text"],
                        "type": entity["Type"],
                    },
                    f"{folders['entities']}{name}_review{i}_{entity['Text']}"
                )
            print(f"{name}({i}): {len(entities['Entities'])} entities analysis uploaded to S3 ({S3_BUCKET})")


            # Detect sentiment by entity
            targeted_sentiment = COMPREHEND.detect_targeted_sentiment(
                Text=review_text,
                LanguageCode="en",
            )
            for target in targeted_sentiment["Entities"]:
                descriptionIndex = target["DescriptiveMentionIndex"][0]
                description = target["Mentions"][descriptionIndex]

                upload_to_s3(
                    {
                        "name": name,
                        "entity": description["Text"],
                        "type": description["Type"],
                        "sentiment": description["MentionSentiment"]["Sentiment"]
                    },
                    f"{folders['targeted_sentiment']}{name}_review{i}_{description['Text']}"
                )
            print(f"{name}({i}): {len(targeted_sentiment['Entities'])} targeted sentiment analysis uploaded to S3 ({S3_BUCKET})")


    # Start AWS Glue Crawler
    try:
        GLUE.start_crawler(Name=GLUE_CRAWLER)
        print(f"Successfully started Glue crawler: {GLUE_CRAWLER}")
    except Exception as e:
        print(f"Error starting Glue crawler: {str(e)}")


    # Safely exit Lambda function
    return { 
        "statusCode": 200,
        "body": f"Analysis completed, data uploaded to S3 and Glue crawler started.\nReceived {len(places)} places: {json.dumps(places, indent=2)}"
    }
