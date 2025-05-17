variable "environment" {
  description = "Environment name (dev, stage, prod)"
  type        = string
}

variable "lambda_function_arns" {
  description = "ARNs of the Lambda functions to integrate with API Gateway"
  type        = map(string)
}

variable "lambda_authorizer_role_arn" {
  description = "ARN of the IAM role for Lambda authorizer"
  type        = string
} 