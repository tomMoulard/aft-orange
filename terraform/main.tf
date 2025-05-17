terraform {
  required_version = ">= 1.0.0"
  
  backend "s3" {
    # This will be configured per environment
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = var.default_tags
  }
}

# Cognito User Pool for authentication
module "cognito" {
  source = "./modules/cognito"
  
  environment = var.environment
}

# IAM module
module "iam" {
  source = "./modules/iam"
  
  environment = var.environment
}

# Lambda module
module "lambda" {
  source = "./modules/lambda"
  
  environment = var.environment
  iam_role_arn = module.iam.lambda_role_arn
  
  # GitLab configuration
  gitlab_url = var.gitlab_url
  gitlab_project_id = var.gitlab_project_id
  gitlab_branch = var.gitlab_branch
  
  # Cognito configuration
  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_app_client_id = module.cognito.user_pool_client_id
}

# API Gateway module
module "api_gateway" {
  source = "./modules/api_gateway"
  
  environment = var.environment
  lambda_function_arns = module.lambda.function_arns
  lambda_authorizer_role_arn = module.iam.lambda_authorizer_role_arn
} 