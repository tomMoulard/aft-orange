output "api_gateway_url" {
  description = "URL of the deployed API Gateway"
  value       = module.api_gateway.api_url
}

output "api_gateway_id" {
  description = "ID of the deployed API Gateway"
  value       = module.api_gateway.api_id
}

output "lambda_function_names" {
  description = "Names of the deployed Lambda functions"
  value       = module.lambda.function_names
} 