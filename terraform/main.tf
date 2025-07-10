provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ai-api-rg"
  location = "East US"
}
