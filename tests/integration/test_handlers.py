import json
import os
import pytest
from unittest.mock import patch

from handlers.account_handlers import create_account_handler
from tests.fixtures.account_requests import VALID_CREATE_REQUEST


class MockContext:
    def __init__(self):
        self.function_name = "test-function"
        self.aws_request_id = "test-request-id"


@pytest.mark.integration
@patch("utils.gitlab_client.GitLabClient")
def test_create_account_handler_success(mock_gitlab_client):
    """Test successful account creation handler execution"""
    # Setup mock GitLab client
    mock_instance = mock_gitlab_client.return_value
    mock_instance.commit_config_files.return_value = "abc123"
    
    # Create test event
    event = {
        "body": json.dumps(VALID_CREATE_REQUEST)
    }
    
    # Execute handler
    response = create_account_handler(event, MockContext())
    
    # Verify response
    assert response["statusCode"] == 202
    assert "account_name" in json.loads(response["body"])
    assert "commit_sha" in json.loads(response["body"])
    
    # Verify GitLab client was called
    mock_instance.commit_config_files.assert_called_once()


@pytest.mark.integration
def test_create_account_handler_invalid_input():
    """Test account creation handler with invalid input"""
    # Create test event with missing required fields
    event = {
        "body": json.dumps({"account_name": "testaccount"})  # Missing required fields
    }
    
    # Execute handler
    response = create_account_handler(event, MockContext())
    
    # Verify error response
    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"]) 