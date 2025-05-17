terraform {
  required_version = ">= 1.0.0"
  
  backend "s3" {
    bucket         = "aft-api-terraform-state-dev"
    key            = "terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "aft-api-terraform-locks-dev"
    encrypt        = true
  }
}

module "aft_api" {
  source = "../../"
  
  aws_region  = "us-west-2"
  environment = "dev"
  
  default_tags = {
    Project     = "AFT-API"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
} 