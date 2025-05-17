variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, stage, prod)"
  type        = string
}

variable "default_tags" {
  description = "Default tags to apply to all resources"
  type        = map(string)
  default     = {}
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