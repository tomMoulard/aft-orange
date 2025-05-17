output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_authorizer_role_arn" {
  description = "ARN of the Lambda authorizer role"
  value       = aws_iam_role.lambda_authorizer_role.arn
} 