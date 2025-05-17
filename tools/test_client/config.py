"""Configuration for the AFT API test client"""
import os
from typing import Dict, Optional

# API Gateway configurations for different environments
API_ENDPOINTS = {
    "dev": "https://api-dev.example.com",
    "stage": "https://api-stage.example.com",
    "prod": "https://api-prod.example.com",
}

# Default environment to use
DEFAULT_ENV = "dev"

# API paths
API_PATHS = {
    "create_account": "/accounts",
    "update_account": "/accounts/{account_name}",
    "delete_account": "/accounts/{account_name}",
}

def get_api_url(environment: Optional[str] = None) -> str:
    """Get the API URL for the specified environment"""
    env = environment or os.environ.get("AFT_API_ENV", DEFAULT_ENV)
    return API_ENDPOINTS.get(env, API_ENDPOINTS[DEFAULT_ENV]) 