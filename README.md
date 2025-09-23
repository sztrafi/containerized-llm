# Azure AI API Gateway

Lightweight containerized FastAPI app exposing **Azure AI Services (Text Analytics)** and **Azure OpenAI (Chat LLM)** through simple REST endpoints.

## Features
- `/sentiment?text=I love this project!` → sentiment analysis
- `/language?text=Das ist ein Test` → language detection
- `/llm?prompt=Write a haiku about clouds` → LLM response from Azure OpenAI

## Project Stack
- **FastAPI** for API Gateway
- **Azure AI Services (Text Analytics)** for classical AI
- **Azure OpenAI** for LLM
- **Terraform** to provision Azure resources
- **Docker** for containerization
- **GitHub Actions** for CI/CD