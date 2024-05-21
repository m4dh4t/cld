# Social Media Monitoring with Amazon Comprehend

## POC Objectives

Validate the use of Amazon Comprehend for real-time social media monitoring to detect trends, popular topics, and crisis alerts.

## Infra Architecture

- Logical Components:
  - User interface for data visualization and alerts.
  - Backend for collecting and processing social media data.
  - Amazon Comprehend for sentiment analysis and entity extraction.
  - Database for storing analyzed data.
- Ports/Protocols:
  - HTTP/HTTPS for API requests from social media platforms and the user interface.
  - Security protocols for user authentication and authorization.
- Type of Cloud:
  - AWS for hosting services and utilizing Amazon Comprehend.

## Scenario

### STEP 01

```text
//given -> the user has configured the application to monitor specific keywords on Twitter

//when -> a new tweet containing one of the keywords is posted

//then -> the application's backend collects the tweet and sends it to Amazon Comprehend for sentiment analysis
```

### STEP 02

```text
//given -> the tweet is sent to Amazon Comprehend

//when -> Amazon Comprehend performs sentiment analysis on the tweet

//then -> the backend stores the sentiment analysis results (positive, negative, neutral, or mixed) in the database
```

### STEP 03

```text
//given -> the sentiment analysis results are stored

//when -> Amazon Comprehend performs entity recognition on the tweet

//then -> the backend stores the recognized entities (e.g., locations, dates, organizations) in the database
```

### STEP 04

```text
//given -> the recognized entities are stored

//when -> Amazon Comprehend performs key phrase extraction on the tweet

//then -> the backend stores the extracted key phrases in the database
```

### STEP 05

```text
//given -> the tweet is fully analyzed with sentiment, entities, and key phrases

//when -> the backend identifies a targeted negative sentiment with specific entities (e.g., organization name) and key phrases

//then -> an alert is generated in the system
```

### STEP 06

```text
//given -> an alert is generated

//when -> the user accesses the user interface

//then -> the user sees the new trends, popular topics, real-time alerts, and detailed insights including sentiment, entities, and key phrases
```

## Cost

<analysis of load-related costs.>

<option to reduce or adapt costs (practices, subscription)>

## Return of experience

<take a position on the poc that has been produced.>

<Did it validate the announced objectives?>
