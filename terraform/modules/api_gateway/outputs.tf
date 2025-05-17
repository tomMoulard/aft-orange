output "api_id" {
  description = "ID of the created API Gateway"
  value       = aws_apigatewayv2_api.aft_api.id
}

output "api_url" {
  description = "URL of the deployed API Gateway"
  value       = aws_apigatewayv2_stage.default.invoke_url
} 