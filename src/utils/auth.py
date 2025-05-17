import json
import os
import time
from typing import Dict, Any, Tuple, Optional

import boto3
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

# Environment variables
USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
APP_CLIENT_ID = os.environ.get('COGNITO_APP_CLIENT_ID')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-1')

# Constants
KEYS_URL = f'https://cognito-idp.{AWS_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'


class AuthError(Exception):
    """Custom exception for authentication errors"""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        super().__init__(self.error)


def get_token_from_header(event: Dict[str, Any]) -> str:
    """
    Extract JWT token from the Authorization header
    
    Args:
        event: Lambda event object
    
    Returns:
        JWT token string
    
    Raises:
        AuthError: If token is missing or invalid
    """
    headers = event.get('headers', {})
    if not headers:
        raise AuthError({"message": "No headers in the request"}, 401)
        
    auth_header = headers.get('Authorization')
    if not auth_header:
        raise AuthError({"message": "Authorization header is missing"}, 401)
    
    auth_parts = auth_header.split()
    if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
        raise AuthError({"message": "Authorization header must be 'Bearer token'"}, 401)
    
    return auth_parts[1]


def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate the JWT token
    
    Args:
        token: JWT token to validate
    
    Returns:
        Dict containing the decoded JWT claims
    
    Raises:
        AuthError: If the token validation fails
    """
    # Get the JWKs from Cognito
    try:
        jwks_response = requests.get(KEYS_URL)
        jwks = jwks_response.json()['keys']
    except Exception as e:
        raise AuthError({"message": f"Failed to fetch JWT keys: {str(e)}"}, 500) from e

    # Get the header of the JWT
    try:
        header = jwt.get_unverified_header(token)
    except Exception as e:
        raise AuthError({"message": f"Invalid JWT token header: {str(e)}"}, 401) from e

    # Find the JWK that matches the KID in the JWT header
    rsa_key = {}
    for key in jwks:
        if key["kid"] == header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if not rsa_key:
        raise AuthError({"message": "Unable to find matching JWT key"}, 401)

    try:
        # Verify the signature
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=APP_CLIENT_ID,
            issuer=f'https://cognito-idp.{AWS_REGION}.amazonaws.com/{USER_POOL_ID}'
        )
        
        # Verify token is not expired
        current_time = time.time()
        if payload.get('exp') and current_time > payload['exp']:
            raise AuthError({"message": "Token is expired"}, 401)
        
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({"message": "Token is expired"}, 401)
    except jwt.JWTClaimsError as e:
        raise AuthError({"message": f"Invalid claims: {str(e)}"}, 401) from e
    except Exception as e:
        raise AuthError({"message": f"Invalid token: {str(e)}"}, 401) from e


def check_permissions(claims: Dict[str, Any], required_permission: str) -> bool:
    """
    Check if the user has the required permissions
    
    Args:
        claims: JWT claims from the token
        required_permission: Permission required for this action
    
    Returns:
        Boolean indicating if user has permission
    """
    # Get user groups from the token
    cognito_groups = claims.get('cognito:groups', [])
    
    # For now, we have a simple permission model:
    # - Administrators can do anything
    # - Readers can only read
    if required_permission == 'read':
        return 'Administrators' in cognito_groups or 'Readers' in cognito_groups
    else:  # For write permissions
        return 'Administrators' in cognito_groups
    
    # In a more complex scenario, we could have finer-grained permissions
    # mapped to specific operations 