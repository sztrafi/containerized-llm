from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

AZURE_COG_ENDPOINT = os.getenv("AZURE_COG_ENDPOINT")
AZURE_COG_KEY = os.getenv("AZURE_COG_KEY")

@app.get("/llm")
def call_llm(prompt: str):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    body = {
        "prompt": prompt,
        "max_tokens": 50
    }
    try:
        response = requests.post(f"{AZURE_OPENAI_ENDPOINT}/completions", headers=headers, json=body)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cognitive")
def call_cognitive(text: str):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_COG_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "documents": [{"id": "1", "language": "en", "text": text}]
    }
    try:
        response = requests.post(f"{AZURE_COG_ENDPOINT}/text/analytics/v3.0/sentiment", headers=headers, json=body)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

