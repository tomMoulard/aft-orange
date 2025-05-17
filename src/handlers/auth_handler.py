import json
import logging
from typing import Dict, Any, Optional

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

from utils.auth import get_token_from_header, validate_token, check_permissions, AuthError

logger = Logger()
tracer = Tracer()

# Define API permissions map - mapping HTTP methods to required permissions
API_PERMISSIONS = {
    "GET": "read",
    "POST": "write",
    "PUT": "write",
    "DELETE": "write"
}

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_authorizer(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda authorizer for API Gateway
    
    Args:
        event: Lambda event
        context: Lambda context
        
    Returns:
        Authorization response
    """
    logger.debug("Authorization request", extra={"event": event})
    
    # Extract request parameters
    method_arn = event.get("methodArn", "")
    
    try:
        # Get token from authorization header
        token = get_token_from_header(event)
        
        # Validate token
        claims = validate_token(token)
        logger.debug("Token validated successfully", extra={"claims": claims})
        
        # Get HTTP method for permission check
        method = event.get("requestContext", {}).get("http", {}).get("method", "")
        required_permission = API_PERMISSIONS.get(method, "write")  # Default to write permission
        
        # Check if user has required permissions
        if not check_permissions(claims, required_permission):
            logger.warning("Permission denied", extra={
                "user": claims.get("email"),
                "required_permission": required_permission
            })
            raise AuthError({"message": "User does not have required permissions"}, 403)
        
        # Generate policy
        policy = generate_policy(
            principal_id=claims.get("sub", "user"),
            effect="Allow",
            resource=method_arn,
            context={
                "email": claims.get("email", ""),
                "groups": ",".join(claims.get("cognito:groups", [])),
            }
        )
        
        return policy
    except AuthError as e:
        logger.error(f"Authorization error: {str(e)}", extra={"error": e.error, "status_code": e.status_code})
        # For token validation errors, deny access
        return generate_policy(
            principal_id="user",
            effect="Deny",
            resource=method_arn
        )
    except Exception as e:
        # For unexpected errors, log and deny access
        logger.exception(f"Unexpected error in authorizer: {str(e)}")
        return generate_policy(
            principal_id="user",
            effect="Deny",
            resource=method_arn
        )


def generate_policy(principal_id: str, effect: str, resource: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generate IAM policy document for API Gateway
    
    Args:
        principal_id: User identifier
        effect: Allow or Deny
        resource: Resource ARN
        context: Additional context to pass to API Gateway
        
    Returns:
        Policy document
    """
    policy = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
    
    # Add context if provided
    if context:
        policy["context"] = context
    
    return policy 