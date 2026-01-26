# Document Intelligence Pipeline

[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform)](terraform/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)](Dockerfile)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](api/)
[![Azure](https://img.shields.io/badge/Cloud-Azure-0078D4?logo=microsoftazure)](https://azure.microsoft.com)

A project for processing documents, using cloud services, Terraform, and DevOps practices.

> **Note**: This project showcases infrastructure design and DevOps practices. Azure subscription required for full deployment. Local demo available without Azure.

## Architecture

```
┌──────────────┐    ┌─────────────┐    ┌──────────────────┐    ┌────────────┐
│   GitHub     │───▶│  Terraform  │───▶│  Azure Cloud     │───▶│  End User  │
│              │    │             │    │                  │    │            │
│ • Source     │    │ • Resources │    │ • ACR            │    │ • Upload   │
│ • Workflows  │    │ • State     │    │ • Container Apps │    │ • Analyze  │
│ • IaC        │    │ • Outputs   │    │ • AI Services    │    │ • Insights │
└──────────────┘    └─────────────┘    └──────────────────┘    └────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Application** | Python 3.11, Streamlit | Document processing interface |
| **AI Services** | Azure Document Intelligence, Azure OpenAI | Text extraction, insight generation |
| **Infrastructure** | Terraform | Declarative infrastructure provisioning |
| **Container** | Docker, Azure Container Registry | Application packaging and distribution |
| **Orchestration** | Azure Container Apps | Serverless container hosting |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure CLI (`az`)
- Terraform (`>= 1.5.0`)
- Active Azure subscription (for cloud deployment)

### Local Development (No Azure Required)

```bash
# Clone repository
git clone https://github.com/sztrafi/containerized-llm.git
cd containerized-llm

# Start application
docker-compose up --build

# Access at http://localhost:8501
```

The application runs in **local mode** with mock data for demonstration purposes.

## Infrastructure Deployment

### 1. Azure Authentication

```bash
# Login to Azure
az login

# Set active subscription
az account list --output table
az account set --subscription "<your-subscription-id>"

# Register required providers
az provider register --namespace Microsoft.App
```

### 2. Provision Infrastructure

```bash
cd terraform

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure
terraform apply -auto-approve
```

**Resources Created:**
- Resource Group (`ai-api-rg`)
- Container Registry (`aiapigatewayacr`)
- Container App Environment (`aiapienv`)
- Container App (`aiapigateway`)
- Azure AI Services (Text Analytics)

### 3. Configure Container Registry Access

```bash
# Get Container App managed identity
PRINCIPAL_ID=$(az containerapp show \
  --name aiapigateway \
  --resource-group ai-api-rg \
  --query identity.principalId -o tsv)

# Grant ACR pull permissions
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role AcrPull \
  --scope /subscriptions/<subscription-id>/resourceGroups/ai-api-rg/providers/Microsoft.ContainerRegistry/registries/aiapigatewayacr
```

### 4. Build and Deploy Container

```bash
# Enable ACR admin access
az acr update -n aiapigatewayacr --admin-enabled true

# Get ACR credentials
az acr credential show -n aiapigatewayacr

# Login to registry
docker login aiapigatewayacr.azurecr.io -u aiapigatewayacr -p <password>

# Build and push image
docker build -t aiapigatewayacr.azurecr.io/ai-api:latest .
docker push aiapigatewayacr.azurecr.io/ai-api:latest
```

### 5. Configure AI Services

**Option A: Azure Portal**
1. Navigate to Azure AI Foundry
2. Create Hub + Project
3. Deploy model (for example GPT-3.5-turbo or GPT-4)
4. Copy endpoint and API key

**Option B: Azure CLI**
```bash
# Get cognitive services endpoint
az cognitiveservices account show \
  --name aiapigatewaycog \
  --resource-group ai-api-rg \
  --query properties.endpoint -o tsv

# Get cognitive services key
az cognitiveservices account keys list \
  --name aiapigatewaycog \
  --resource-group ai-api-rg \
  --query key1 -o tsv
```

### 6. Environment Configuration

Create `.env` file:

```bash
AI_SERVICE_ENDPOINT=https://aiapigatewaycog.cognitiveservices.azure.com/
AI_SERVICE_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=https://<your-openai>.openai.azure.com/
AZURE_OPENAI_KEY=<your-key>
```

## Project Structure

```
containerized-llm/
├── api/
│   ├── src/
│   │   └── app.py              # Streamlit application
│   └── requirements.txt        # Python dependencies
├── terraform/
│   ├── main.tf                 # Infrastructure definitions
│   ├── variables.tf            # Configuration variables
│   └── outputs.tf              # Resource outputs
├── .github/
│   └── workflows/              # CI/CD pipelines
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local development setup
└── README.md                   # This file
```

## Development Workflow

```bash
# Local development with hot reload
docker-compose up

# Validate Terraform
cd terraform
terraform fmt -check
terraform validate

# Build container
docker build -t llm-app:local .

# Run container
docker run -p 8501:8501 llm-app:local
```

## Contact

**Filip Sztramski**
- GitHub: [@sztrafi](https://github.com/sztrafi)
- LinkedIn: https://www.linkedin.com/in/filip-sztramski/

---
