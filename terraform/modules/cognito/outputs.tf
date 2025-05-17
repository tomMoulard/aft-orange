output "user_pool_id" {
  description = "ID of the Cognito User Pool"
  value       = aws_cognito_user_pool.aft_user_pool.id
}

output "user_pool_client_id" {
  description = "ID of the Cognito User Pool Client"
  value       = aws_cognito_user_pool_client.aft_client.id
}

output "admin_group_name" {
  description = "Name of the administrators group"
  value       = aws_cognito_user_group.admin_group.name
}

output "reader_group_name" {
  description = "Name of the readers group"
  value       = aws_cognito_user_group.reader_group.name
} 