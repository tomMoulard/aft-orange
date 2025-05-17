import json
import pytest

from models.account import AccountRequest
from utils.config_generator import ConfigGenerator


def test_generate_account_config_basic():
    """Test basic account config generation"""
    # Given
    account_request = AccountRequest(
        account_name="testaccount",
        email="test@example.com",
        organizational_unit="Sandbox"
    )
    
    # When
    generator = ConfigGenerator()
    config_files = generator.generate_account_config(account_request)
    
    # Then
    assert len(config_files) == 2
    
    # Request file
    request_file = next(f for f in config_files if f.file_path.endswith('request.json'))
    assert request_file is not None
    request_content = json.loads(request_file.content)
    assert request_content["name"] == "testaccount"
    assert request_content["email"] == "test@example.com"
    assert request_content["organizational_unit"] == "Sandbox"
    
    # Customizations file
    custom_file = next(f for f in config_files if f.file_path.endswith('customizations.json'))
    assert custom_file is not None
    custom_content = json.loads(custom_file.content)
    assert custom_content["sso_user"] is None


def test_generate_account_config_with_sso():
    """Test account config generation with SSO user"""
    # Given
    account_request = AccountRequest(
        account_name="testaccount",
        email="test@example.com",
        organizational_unit="Sandbox",
        sso_user_email="sso@example.com",
        sso_user_first_name="Test",
        sso_user_last_name="User"
    )
    
    # When
    generator = ConfigGenerator()
    config_files = generator.generate_account_config(account_request)
    
    # Then
    custom_file = next(f for f in config_files if f.file_path.endswith('customizations.json'))
    custom_content = json.loads(custom_file.content)
    assert custom_content["sso_user"] is not None
    assert custom_content["sso_user"]["email"] == "sso@example.com"
    assert custom_content["sso_user"]["first_name"] == "Test"
    assert custom_content["sso_user"]["last_name"] == "User" 