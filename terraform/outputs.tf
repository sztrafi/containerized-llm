output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "cognitive_endpoint" {
  value = azurerm_cognitive_account.ai.endpoint
}

output "cognitive_key" {
  value = azurerm_cognitive_account.ai.primary_access_key
}
