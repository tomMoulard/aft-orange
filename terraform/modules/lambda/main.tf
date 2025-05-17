locals {
  common_lambda_config = {
    runtime       = "python3.9"
    timeout       = 30
    memory_size   = 128
    architecture  = ["x86_64"]
  }
  
  lambda_functions = {
    create_account = {
      description = "Lambda function to handle account creation requests"
      handler     = "handlers.account_handlers.create_account_handler"
    },
    update_account = {
      description = "Lambda function to handle account update requests"
      handler     = "handlers.account_handlers.update_account_handler"
    },
    delete_account = {
      description = "Lambda function to handle account deletion requests"
      handler     = "handlers.account_handlers.delete_account_handler"
    },
    upgrade_account = {
      description = "Lambda function to handle account upgrade requests"
      handler     = "handlers.account_handlers.upgrade_account_handler"
    },
    downgrade_account = {
      description = "Lambda function to handle account downgrade requests"
      handler     = "handlers.account_handlers.downgrade_account_handler"
    },
    add_option = {
      description = "Lambda function to handle adding options to accounts"
      handler     = "handlers.account_handlers.add_option_handler"
    },
    remove_option = {
      description = "Lambda function to handle removing options from accounts"
      handler     = "handlers.account_handlers.remove_option_handler"
    }
  }
}

# Create a zip file of the Lambda source code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../src"
  output_path = "${path.module}/lambda_function.zip"
}

# Create Lambda functions
resource "aws_lambda_function" "functions" {
  for_each = local.lambda_functions
  
  function_name    = "aft-api-${each.key}-${var.environment}"
  description      = each.value.description
  role             = var.iam_role_arn
  handler          = each.value.handler
  runtime          = local.common_lambda_config.runtime
  timeout          = local.common_lambda_config.timeout
  memory_size      = local.common_lambda_config.memory_size
  architectures    = local.common_lambda_config.architecture
  
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  
  environment {
    variables = {
      ENVIRONMENT = var.environment
      LOG_LEVEL   = var.environment == "prod" ? "INFO" : "DEBUG"
      GITLAB_URL  = var.gitlab_url
      GITLAB_PROJECT_ID = var.gitlab_project_id
      GITLAB_BRANCH = var.gitlab_branch
      COGNITO_USER_POOL_ID = var.cognito_user_pool_id
      COGNITO_APP_CLIENT_ID = var.cognito_app_client_id
    }
  }
  
  tags = {
    Environment = var.environment
    Function    = each.key
  }
}

# CloudWatch Log Groups for Lambda functions
resource "aws_cloudwatch_log_group" "lambda_logs" {
  for_each = local.lambda_functions
  
  name              = "/aws/lambda/aft-api-${each.key}-${var.environment}"
  retention_in_days = 30
  
  tags = {
    Environment = var.environment
    Function    = each.key
  }
} 