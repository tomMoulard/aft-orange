import json
import os
from typing import Dict, List, Any, Optional

import jinja2

from models.account import AccountConfigFile, AccountRequest


class ConfigGenerator:
    """Factory for generating AFT configuration files"""

    def __init__(self):
        self.template_loader = jinja2.FileSystemLoader(searchpath="templates")
        self.template_env = jinja2.Environment(loader=self.template_loader)

    def generate_account_config(
        self, account_request: AccountRequest, update: bool = False
    ) -> List[AccountConfigFile]:
        """
        Generate configuration files for an account.
        
        Args:
            account_request: The account request data
            update: Whether this is an update operation
            
        Returns:
            List of configuration files to commit
        """
        # This is a placeholder for the actual implementation
        # In a real implementation, this would use templates to generate the configuration files
        
        # Example implementation (to be replaced with actual template-based generation)
        account_name = account_request.account_name
        base_path = f"aft-account-request/{account_name}"
        
        # Account request file
        account_request_content = {
            "name": account_request.account_name,
            "email": account_request.email,
            "organizational_unit": account_request.organizational_unit,
            "account_tags": account_request.account_tags or {},
            "custom_fields": account_request.custom_fields or {},
        }
        
        # Account customizations file
        account_customizations_content = {
            "custom_fields": account_request.custom_fields or {},
            "sso_user": None,
        }
        
        # Add SSO user if provided
        if account_request.sso_user_email:
            account_customizations_content["sso_user"] = {
                "email": account_request.sso_user_email,
                "first_name": account_request.sso_user_first_name,
                "last_name": account_request.sso_user_last_name,
            }
        
        # Create the configuration files
        config_files = [
            AccountConfigFile(
                file_path=f"{base_path}/request.json",
                content=json.dumps(account_request_content, indent=2),
            ),
            AccountConfigFile(
                file_path=f"{base_path}/customizations.json",
                content=json.dumps(account_customizations_content, indent=2),
            ),
        ]
        
        return config_files
        
    def generate_upgrade_config(self, account_name: str, target_tier: str) -> List[AccountConfigFile]:
        """
        Generate configuration files for upgrading an account to a higher tier.
        
        Args:
            account_name: The name of the account to upgrade
            target_tier: The target tier for the upgrade
            
        Returns:
            List of configuration files to commit
        """
        base_path = f"aft-account-request/{account_name}"
        
        # Create upgrade configuration
        upgrade_config = {
            "operation": "upgrade",
            "target_tier": target_tier,
            "timestamp": "",  # Will be filled by GitLab client
        }
        
        config_files = [
            AccountConfigFile(
                file_path=f"{base_path}/operations/upgrade.json",
                content=json.dumps(upgrade_config, indent=2),
            ),
        ]
        
        return config_files
    
    def generate_downgrade_config(self, account_name: str, target_tier: str) -> List[AccountConfigFile]:
        """
        Generate configuration files for downgrading an account to a lower tier.
        
        Args:
            account_name: The name of the account to downgrade
            target_tier: The target tier for the downgrade
            
        Returns:
            List of configuration files to commit
        """
        base_path = f"aft-account-request/{account_name}"
        
        # Create downgrade configuration
        downgrade_config = {
            "operation": "downgrade",
            "target_tier": target_tier,
            "timestamp": "",  # Will be filled by GitLab client
        }
        
        config_files = [
            AccountConfigFile(
                file_path=f"{base_path}/operations/downgrade.json",
                content=json.dumps(downgrade_config, indent=2),
            ),
        ]
        
        return config_files
    
    def generate_add_option_config(
        self, account_name: str, option_name: str, option_config: Dict[str, Any]
    ) -> List[AccountConfigFile]:
        """
        Generate configuration files for adding an option to an account.
        
        Args:
            account_name: The name of the account
            option_name: The name of the option to add
            option_config: Configuration details for the option
            
        Returns:
            List of configuration files to commit
        """
        base_path = f"aft-account-request/{account_name}"
        
        # Create option configuration
        option_content = {
            "name": option_name,
            "config": option_config,
            "enabled": True,
            "timestamp": "",  # Will be filled by GitLab client
        }
        
        config_files = [
            AccountConfigFile(
                file_path=f"{base_path}/options/{option_name}.json",
                content=json.dumps(option_content, indent=2),
            ),
        ]
        
        return config_files
    
    def generate_remove_option_config(self, account_name: str, option_name: str) -> List[AccountConfigFile]:
        """
        Generate configuration files for removing an option from an account.
        The implementation actually sets the option as disabled instead of deleting it.
        
        Args:
            account_name: The name of the account
            option_name: The name of the option to remove
            
        Returns:
            List of configuration files to commit
        """
        base_path = f"aft-account-request/{account_name}"
        
        # Create option configuration with enabled=False
        option_content = {
            "name": option_name,
            "enabled": False,
            "timestamp": "",  # Will be filled by GitLab client
        }
        
        config_files = [
            AccountConfigFile(
                file_path=f"{base_path}/options/{option_name}.json",
                content=json.dumps(option_content, indent=2),
            ),
        ]
        
        return config_files 