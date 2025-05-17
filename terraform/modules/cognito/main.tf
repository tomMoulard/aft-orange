resource "aws_cognito_user_pool" "aft_user_pool" {
  name = "aft-user-pool-${var.environment}"
  
  username_attributes      = ["email"]
  auto_verify_attributes   = ["email"]
  
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }
  
  schema {
    name                = "role"
    attribute_data_type = "String"
    mutable             = true
    required            = false
    
    string_attribute_constraints {
      min_length = 1
      max_length = 255
    }
  }
  
  admin_create_user_config {
    allow_admin_create_user_only = true
  }
  
  tags = {
    Environment = var.environment
  }
}

resource "aws_cognito_user_pool_client" "aft_client" {
  name                = "aft-api-client-${var.environment}"
  user_pool_id        = aws_cognito_user_pool.aft_user_pool.id
  
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
  
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
  
  access_token_validity  = 60
  id_token_validity      = 60
  refresh_token_validity = 30
  
  prevent_user_existence_errors = "ENABLED"
  supported_identity_providers  = ["COGNITO"]
  
  callback_urls = ["https://example.com/callback"]
  logout_urls   = ["https://example.com/logout"]
}

resource "aws_cognito_user_group" "admin_group" {
  name         = "Administrators"
  description  = "Administrators with full access"
  user_pool_id = aws_cognito_user_pool.aft_user_pool.id
  precedence   = 1
}

resource "aws_cognito_user_group" "reader_group" {
  name         = "Readers"
  description  = "Read-only users"
  user_pool_id = aws_cognito_user_pool.aft_user_pool.id
  precedence   = 2
} 