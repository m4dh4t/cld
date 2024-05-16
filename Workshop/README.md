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

//then -> the application's backend collects the tweet and sends it to Amazon Comprehend for analysis
```

### STEP 02

```text
//given -> the tweet is analyzed by Amazon Comprehend

//when -> the analysis results are available

//then -> the backend stores the results in the database and generates an alert if a negative sentiment is detected
```

### STEP 03

```text
//given -> an alert is generated

//when -> the user accesses the user interface

//then -> the user sees new trends, popular topics, and real-time alerts
```

## Cost

<analysis of load-related costs.>

<option to reduce or adapt costs (practices, subscription)>

## Return of experience

<take a position on the poc that has been produced.>

<Did it validate the announced objectives?>
