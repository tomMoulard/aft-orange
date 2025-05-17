from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AccountRequest(BaseModel):
    """Account request model for AFT API"""
    account_name: str = Field(..., description="Name of the account", min_length=1, max_length=50)
    email: str = Field(..., description="Email address for the AWS account")
    organizational_unit: str = Field(..., description="OU where the account will be placed")
    account_tags: Dict[str, str] = Field(default_factory=dict, description="Tags to apply to the account")
    custom_fields: Dict[str, str] = Field(default_factory=dict, description="Custom fields for account configuration")
    sso_user_email: Optional[str] = Field(None, description="Email for SSO user access")
    sso_user_first_name: Optional[str] = Field(None, description="First name for SSO user")
    sso_user_last_name: Optional[str] = Field(None, description="Last name for SSO user")


class AccountConfigFile(BaseModel):
    """Model representing an AFT configuration file"""
    file_path: str
    content: str 