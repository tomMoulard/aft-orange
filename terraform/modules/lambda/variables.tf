variable "environment" {
  description = "Environment name (dev, stage, prod)"
  type        = string
}

variable "iam_role_arn" {
  description = "ARN of the IAM role to be used by the Lambda functions"
  type        = string
}

variable "gitlab_url" {
  description = "GitLab URL for API access"
  type        = string
}

variable "gitlab_project_id" {
  description = "GitLab project ID"
  type        = string
}

variable "gitlab_branch" {
  description = "GitLab branch to use"
  type        = string
  default     = "main"
}

variable "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  type        = string
}

variable "cognito_app_client_id" {
  description = "Cognito App Client ID"
  type        = string
} 