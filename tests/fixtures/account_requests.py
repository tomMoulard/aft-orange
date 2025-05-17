"""Test fixtures for account requests"""

VALID_CREATE_REQUEST = {
    "account_name": "testaccount",
    "email": "test@example.com",
    "organizational_unit": "Sandbox",
    "account_tags": {
        "Environment": "Test",
        "CostCenter": "12345"
    },
    "custom_fields": {
        "vpc_cidr": "10.0.0.0/16",
        "region": "us-west-2"
    }
}

VALID_CREATE_REQUEST_WITH_SSO = {
    "account_name": "testaccount",
    "email": "test@example.com",
    "organizational_unit": "Sandbox",
    "account_tags": {
        "Environment": "Test",
        "CostCenter": "12345"
    },
    "custom_fields": {
        "vpc_cidr": "10.0.0.0/16",
        "region": "us-west-2"
    },
    "sso_user_email": "sso@example.com",
    "sso_user_first_name": "Test",
    "sso_user_last_name": "User"
}

INVALID_REQUEST_MISSING_OU = {
    "account_name": "testaccount",
    "email": "test@example.com"
}

INVALID_REQUEST_BAD_NAME = {
    "account_name": "test-account",  # Contains hyphen which is not alphanumeric
    "email": "test@example.com",
    "organizational_unit": "Sandbox"
}

INVALID_REQUEST_BAD_EMAIL = {
    "account_name": "testaccount",
    "email": "testexample.com",  # Missing @ symbol
    "organizational_unit": "Sandbox"
}

VALID_DELETE_REQUEST = {
    "account_name": "testaccount"
} 