from typing import Optional

from models.account import AccountRequest


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_account_request(
    account_request: AccountRequest, update: bool = False
) -> None:
    """
    Validate account request data
    
    Args:
        account_request: The account request to validate
        update: Whether this is an update operation
    
    Raises:
        ValidationError: If validation fails
    """
    # Validate account name format
    if not account_request.account_name.isalnum():
        raise ValidationError("Account name must be alphanumeric")
    
    # Validate email format
    if "@" not in account_request.email:
        raise ValidationError("Invalid email format")
    
    # Validate organizational unit
    if not account_request.organizational_unit:
        raise ValidationError("Organizational unit is required")
    
    # Validate SSO user information
    if account_request.sso_user_email:
        if not account_request.sso_user_first_name or not account_request.sso_user_last_name:
            raise ValidationError("SSO user first and last name are required when SSO email is provided")
    
    # Additional custom validations would go here 