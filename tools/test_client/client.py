"""Test client for AFT API"""
import json
import logging
from typing import Any, Dict, Optional

import requests

from tools.test_client.config import API_PATHS, get_api_url

logger = logging.getLogger(__name__)


class AFTAPIClient:
    """Client for interacting with the AFT API"""
    
    def __init__(self, environment: Optional[str] = None):
        """
        Initialize the client
        
        Args:
            environment: The environment to target (dev, stage, prod)
        """
        self.base_url = get_api_url(environment)
        logger.info(f"Initialized AFT API client for {self.base_url}")
    
    def create_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new AWS account
        
        Args:
            account_data: Account request data
            
        Returns:
            API response
        """
        url = f"{self.base_url}{API_PATHS['create_account']}"
        logger.info(f"Creating account with name: {account_data.get('account_name')}")
        
        response = requests.post(url, json=account_data)
        response.raise_for_status()
        
        return response.json()
    
    def update_account(self, account_name: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing AWS account
        
        Args:
            account_name: Name of the account to update
            account_data: Updated account data
            
        Returns:
            API response
        """
        url = f"{self.base_url}{API_PATHS['update_account']}".format(account_name=account_name)
        logger.info(f"Updating account: {account_name}")
        
        response = requests.put(url, json=account_data)
        response.raise_for_status()
        
        return response.json()
    
    def delete_account(self, account_name: str) -> Dict[str, Any]:
        """
        Delete an AWS account
        
        Args:
            account_name: Name of the account to delete
            
        Returns:
            API response
        """
        url = f"{self.base_url}{API_PATHS['delete_account']}".format(account_name=account_name)
        logger.info(f"Deleting account: {account_name}")
        
        response = requests.delete(url, json={"account_name": account_name})
        response.raise_for_status()
        
        return response.json() 