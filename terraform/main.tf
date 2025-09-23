provider "azurerm" {
  features {}
}

variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "ai-api-rg"
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "aiapigatewayacr"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# Azure AI Services (Text Analytics)
resource "azurerm_cognitive_account" "ai" {
  name                = "aiapigatewaycog"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  kind                = "TextAnalytics"
  sku_name            = "S"
}

# Azure Container App Environment
resource "azurerm_container_app_environment" "env" {
  name                = "aiapienv"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Container App
resource "azurerm_container_app" "app" {
  name                         = "aiapigateway"
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.env.id
  revision_mode                = "Single"

  template {
    container {
      name   = "api"
      image  = "${azurerm_container_registry.acr.login_server}/ai-api:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "AI_SERVICE_ENDPOINT"
        value = azurerm_cognitive_account.ai.endpoint
      }
      env {
        name  = "AI_SERVICE_KEY"
        value = azurerm_cognitive_account.ai.primary_access_key
      }
    }
  }
}
