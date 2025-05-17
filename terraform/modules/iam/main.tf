data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Main Lambda execution role
resource "aws_iam_role" "lambda_role" {
  name = "aft-api-lambda-role-${var.environment}"
  
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
  
  tags = {
    Environment = var.environment
  }
}

# Basic Lambda execution policy
resource "aws_iam_role_policy" "lambda_execution_policy" {
  name = "lambda-execution-policy"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

# Authorizer execution role
resource "aws_iam_role" "lambda_authorizer_role" {
  name = "aft-api-authorizer-role-${var.environment}"
  
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
  
  tags = {
    Environment = var.environment
  }
}

# Authorizer execution policy with Cognito permissions
resource "aws_iam_role_policy" "lambda_authorizer_policy" {
  name = "lambda-authorizer-policy"
  role = aws_iam_role.lambda_authorizer_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action = [
          "cognito-idp:DescribeUserPool",
          "cognito-idp:DescribeUserPoolClient"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
} 