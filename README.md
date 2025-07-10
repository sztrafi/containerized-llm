# containerized-llm
Containerized LLM & Cognitive Service Workflow on Azure project.


# Azure AI API Gateway

Lightweight API gateway exposing Azure OpenAI and Cognitive Services functionality via containerized FastAPI app.

## Features
- `/llm` - Call Azure OpenAI GPT endpoint
- `/cognitive` - Call Azure Cognitive Service Sentiment Analysis

## Deployment
Provision infra with Terraform, containerize app with Docker, deploy to Azure.

