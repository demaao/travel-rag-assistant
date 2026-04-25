from flask import Flask, render_template, request
import boto3
import json

app = Flask(__name__)

# Knowledge Base configuration
KNOWLEDGE_BASE_ID = "D4WDW9CLWV"
REGION = "us-east-1"

# Bedrock clients: one for retrieval, one for generation
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""  # Stores the response shown in the UI

    if request.method == "POST":
        question = request.form.get("question")  # Get user input from form

        try:
            # Retrieve relevant context from Knowledge Base
            retrieve_response = bedrock_agent.retrieve(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                retrievalQuery={"text": question},
                retrievalConfiguration={
                    "vectorSearchConfiguration": {
                        "numberOfResults": 3  # Top-k results
                    }
                }
            )

            #  Extract text content from retrieval results
            contexts = [
                item["content"]["text"]
                for item in retrieve_response.get("retrievalResults", [])
                if "content" in item and "text" in item["content"]
            ]

            # Combine all retrieved chunks into one context string
            context_text = "\n".join(contexts)

            # Build prompt to control answer style
            prompt = f"""
You are a friendly travel assistant.

Answer in a natural, human like paragraph.
Do NOT use bullet points.
Do NOT start with "Based on the search results".

Context:
{context_text}

Question:
{question}

Answer:
"""
            # Generate answer using Bedrock model
            response = bedrock_runtime.invoke_model(
                modelId="amazon.nova-lite-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"text": prompt}  # Chat format required by Nova
                            ]
                        }
                    ]
                })
            )

            #  Parse model response
            result = json.loads(response["body"].read().decode("utf-8"))
            answer = result["output"]["message"]["content"][0]["text"]

            # Clean unwanted phrases if model adds them
            answer = answer.replace("Based on the search results", "").strip()

        except Exception as e:
            answer = f"Error: {str(e)}"

    #  Render HTML with the generated answer
    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)