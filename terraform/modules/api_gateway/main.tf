resource "aws_apigatewayv2_api" "aft_api" {
  name          = "aft-api-${var.environment}"
  protocol_type = "HTTP"
  description   = "API Gateway for AFT account management"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }
  
  tags = {
    Environment = var.environment
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.aft_api.id
  name        = "$default"
  auto_deploy = true
  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format          = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      errorMessage   = "$context.error.message"
    })
  }
  
  tags = {
    Environment = var.environment
  }
}

# JWT Authorizer
resource "aws_apigatewayv2_authorizer" "jwt_authorizer" {
  api_id           = aws_apigatewayv2_api.aft_api.id
  authorizer_type  = "REQUEST"
  identity_sources = ["$request.header.Authorization"]
  name             = "jwt-authorizer"
  
  authorizer_uri           = var.lambda_function_arns["authorizer"]
  authorizer_payload_format_version = "2.0"
  enable_simple_responses  = true
  
  authorizer_credentials_arn = var.lambda_authorizer_role_arn
}

# API Routes for account operations
resource "aws_apigatewayv2_route" "create_account" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "POST /accounts"
  target             = "integrations/${aws_apigatewayv2_integration.create_account.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

resource "aws_apigatewayv2_route" "update_account" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "PUT /accounts/{accountName}"
  target             = "integrations/${aws_apigatewayv2_integration.update_account.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

resource "aws_apigatewayv2_route" "delete_account" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "DELETE /accounts/{accountName}"
  target             = "integrations/${aws_apigatewayv2_integration.delete_account.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

# Routes for account upgrades and downgrades
resource "aws_apigatewayv2_route" "upgrade_account" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "POST /accounts/{accountName}/upgrade"
  target             = "integrations/${aws_apigatewayv2_integration.upgrade_account.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

resource "aws_apigatewayv2_route" "downgrade_account" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "POST /accounts/{accountName}/downgrade"
  target             = "integrations/${aws_apigatewayv2_integration.downgrade_account.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

# Routes for account options management
resource "aws_apigatewayv2_route" "add_option" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "POST /accounts/{accountName}/options"
  target             = "integrations/${aws_apigatewayv2_integration.add_option.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

resource "aws_apigatewayv2_route" "remove_option" {
  api_id             = aws_apigatewayv2_api.aft_api.id
  route_key          = "DELETE /accounts/{accountName}/options/{optionName}"
  target             = "integrations/${aws_apigatewayv2_integration.remove_option.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt_authorizer.id
}

# Lambda integrations
resource "aws_apigatewayv2_integration" "create_account" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["create_account"]
  payload_format_version = "2.0"
  description            = "Create account integration"
}

resource "aws_apigatewayv2_integration" "update_account" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["update_account"]
  payload_format_version = "2.0"
  description            = "Update account integration"
}

resource "aws_apigatewayv2_integration" "delete_account" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["delete_account"]
  payload_format_version = "2.0"
  description            = "Delete account integration"
}

# Additional Lambda integrations
resource "aws_apigatewayv2_integration" "upgrade_account" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["upgrade_account"]
  payload_format_version = "2.0"
  description            = "Upgrade account integration"
}

resource "aws_apigatewayv2_integration" "downgrade_account" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["downgrade_account"]
  payload_format_version = "2.0"
  description            = "Downgrade account integration"
}

resource "aws_apigatewayv2_integration" "add_option" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["add_option"]
  payload_format_version = "2.0"
  description            = "Add account option integration"
}

resource "aws_apigatewayv2_integration" "remove_option" {
  api_id                 = aws_apigatewayv2_api.aft_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arns["remove_option"]
  payload_format_version = "2.0"
  description            = "Remove account option integration"
}

# Lambda permissions
resource "aws_lambda_permission" "create_account_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["create_account"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts"
}

resource "aws_lambda_permission" "update_account_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["update_account"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*"
}

resource "aws_lambda_permission" "delete_account_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["delete_account"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*"
}

# Additional Lambda permissions
resource "aws_lambda_permission" "upgrade_account_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["upgrade_account"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*/upgrade"
}

resource "aws_lambda_permission" "downgrade_account_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["downgrade_account"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*/downgrade"
}

resource "aws_lambda_permission" "add_option_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["add_option"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*/options"
}

resource "aws_lambda_permission" "remove_option_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["remove_option"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/*/*/accounts/*/options/*"
}

# Authorizer lambda permission
resource "aws_lambda_permission" "authorizer_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = element(split(":", var.lambda_function_arns["authorizer"]), 6)
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aft_api.execution_arn}/authorizers/${aws_apigatewayv2_authorizer.jwt_authorizer.id}"
}

resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/apigateway/${aws_apigatewayv2_api.aft_api.name}"
  retention_in_days = 30
  
  tags = {
    Environment = var.environment
  }
} 