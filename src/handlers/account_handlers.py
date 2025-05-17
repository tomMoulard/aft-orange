import json
import logging
from typing import Any, Dict, Optional, Tuple

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

from models.account import AccountRequest
from utils.config_generator import ConfigGenerator
from utils.gitlab_client import GitLabClient
from utils.validators import validate_account_request

logger = Logger()
tracer = Tracer()

def _handle_error(error: Exception) -> Dict[str, Any]:
    """Handle and format error responses"""
    logger.exception("Error processing request")
    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": str(error)})
    }

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def create_account_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for account creation requests"""
    try:
        # Parse and validate the request
        body = json.loads(event.get("body", "{}"))
        account_request = AccountRequest(**body)
        
        validate_account_request(account_request)
        
        # Generate configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_account_config(account_request)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Create account: {account_request.account_name}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Account creation request submitted",
                "account_name": account_request.account_name,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def update_account_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for account update requests"""
    try:
        # Parse and validate the request
        body = json.loads(event.get("body", "{}"))
        account_request = AccountRequest(**body)
        
        validate_account_request(account_request, update=True)
        
        # Generate configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_account_config(account_request, update=True)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Update account: {account_request.account_name}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Account update request submitted",
                "account_name": account_request.account_name,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def delete_account_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for account deletion requests"""
    try:
        # Parse the request
        body = json.loads(event.get("body", "{}"))
        account_name = body.get("account_name")
        
        if not account_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "account_name is required"})
            }
        
        # Delete configuration
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.delete_account_config(
            account_name=account_name,
            commit_message=f"Delete account: {account_name}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Account deletion request submitted",
                "account_name": account_name,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def upgrade_account_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for account upgrade requests"""
    try:
        # Get the account name from the path parameters
        account_name = event.get("pathParameters", {}).get("accountName")
        if not account_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "accountName is required"})
            }
        
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        target_tier = body.get("targetTier")
        
        if not target_tier:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "targetTier is required"})
            }
        
        # Generate upgrade configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_upgrade_config(account_name, target_tier)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Upgrade account {account_name} to {target_tier}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Account upgrade request submitted",
                "account_name": account_name,
                "target_tier": target_tier,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def downgrade_account_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for account downgrade requests"""
    try:
        # Get the account name from the path parameters
        account_name = event.get("pathParameters", {}).get("accountName")
        if not account_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "accountName is required"})
            }
        
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        target_tier = body.get("targetTier")
        
        if not target_tier:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "targetTier is required"})
            }
        
        # Generate downgrade configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_downgrade_config(account_name, target_tier)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Downgrade account {account_name} to {target_tier}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Account downgrade request submitted",
                "account_name": account_name,
                "target_tier": target_tier,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def add_option_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for adding options to an account"""
    try:
        # Get the account name from the path parameters
        account_name = event.get("pathParameters", {}).get("accountName")
        if not account_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "accountName is required"})
            }
        
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        option_name = body.get("optionName")
        option_config = body.get("optionConfig", {})
        
        if not option_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "optionName is required"})
            }
        
        # Generate option configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_add_option_config(account_name, option_name, option_config)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Add option {option_name} to account {account_name}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Add option request submitted",
                "account_name": account_name,
                "option_name": option_name,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e)

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def remove_option_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler for removing options from an account"""
    try:
        # Get the account name and option name from the path parameters
        path_params = event.get("pathParameters", {})
        account_name = path_params.get("accountName")
        option_name = path_params.get("optionName")
        
        if not account_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "accountName is required"})
            }
        
        if not option_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "optionName is required"})
            }
        
        # Generate option removal configuration
        config_generator = ConfigGenerator()
        config_files = config_generator.generate_remove_option_config(account_name, option_name)
        
        # Push to GitLab
        gitlab_client = GitLabClient()
        commit_sha = gitlab_client.commit_config_files(
            config_files=config_files,
            commit_message=f"Remove option {option_name} from account {account_name}"
        )
        
        return {
            "statusCode": 202,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Remove option request submitted",
                "account_name": account_name,
                "option_name": option_name,
                "commit_sha": commit_sha
            })
        }
    except Exception as e:
        return _handle_error(e) 