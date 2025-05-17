import os
from typing import Dict, List

import gitlab

from models.account import AccountConfigFile


class GitLabClientError(Exception):
    """Custom exception for GitLab client errors"""
    pass


class GitLabClient:
    """Client for interacting with GitLab repository"""
    
    def __init__(self):
        # These would come from environment variables or parameter store in real implementation
        self.gitlab_url = os.environ.get("GITLAB_URL")
        self.gitlab_token = os.environ.get("GITLAB_TOKEN")
        self.project_id = os.environ.get("GITLAB_PROJECT_ID")
        self.branch = os.environ.get("GITLAB_BRANCH", "main")
        
        if not self.gitlab_url or not self.gitlab_token or not self.project_id:
            raise ValueError("GitLab configuration missing from environment")
            
        try:
            self.gl = gitlab.Gitlab(url=self.gitlab_url, private_token=self.gitlab_token)
            self.project = self.gl.projects.get(self.project_id)
        except Exception as e:
            raise GitLabClientError(f"Failed to initialize GitLab client: {str(e)}") from e
    
    def commit_config_files(
        self, config_files: List[AccountConfigFile], commit_message: str
    ) -> str:
        """
        Commit configuration files to GitLab
        
        Args:
            config_files: List of configuration files to commit
            commit_message: Commit message
            
        Returns:
            Commit SHA
        """
        try:
            # Create commit data
            commit_data = {
                'branch': self.branch,
                'commit_message': commit_message,
                'actions': []
            }
            
            # Add file actions
            for file in config_files:
                commit_data['actions'].append({
                    'action': 'create',
                    'file_path': file.file_path,
                    'content': file.content,
                })
            
            # Create the commit
            commit = self.project.commits.create(commit_data)
            return commit.id
        except Exception as e:
            raise GitLabClientError(f"Failed to commit files to GitLab: {str(e)}") from e
    
    def delete_account_config(self, account_name: str, commit_message: str) -> str:
        """
        Delete account configuration from GitLab
        
        Args:
            account_name: Name of the account to delete
            commit_message: Commit message
            
        Returns:
            Commit SHA
        """
        try:
            base_path = f"aft-account-request/{account_name}"
            
            # Create commit data to delete files
            commit_data = {
                'branch': self.branch,
                'commit_message': commit_message,
                'actions': [
                    {
                        'action': 'delete',
                        'file_path': f"{base_path}/request.json",
                    },
                    {
                        'action': 'delete',
                        'file_path': f"{base_path}/customizations.json",
                    }
                ]
            }
            
            # Create the commit
            commit = self.project.commits.create(commit_data)
            return commit.id
        except Exception as e:
            raise GitLabClientError(f"Failed to delete account configuration: {str(e)}") from e 