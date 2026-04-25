# Travel RAG Assistant - Dema Omar

## Topic

This project is based on my personal travel experience in Italy.
It focuses on cities, food, and insights from my trip.

---

## Documents Used

The knowledge base includes a small set of documents (9 files) such as:

* Personal travel notes
* Food experiences
* City descriptions (Rome, Naples, Florence)
* Recommendations and observations

These documents were uploaded to Amazon S3 and connected to the Bedrock Knowledge Base.

---

## How the App Works

The application follows a Retrieval-Augmented Generation (RAG) pipeline:

1. The user enters a question in the web interface
2. Flask receives the request
3. boto3 sends the query to Amazon Bedrock
4. The Knowledge Base retrieves relevant document content
5. The Nova Lite model generates a natural answer
6. The answer is displayed in the browser

---

## Public URL (During Testing)

The application was deployed on an EC2 instance and accessed via:

```text id="z9xq2m"
http://34.228.233.151:5000/
```

---

## AWS Resources Deleted

After completing the project, the following resources were deleted:

* EC2 instance
* S3 bucket
* Bedrock Knowledge Base
* OpenSearch Serverless collection

This was done to avoid unnecessary costs.

---
