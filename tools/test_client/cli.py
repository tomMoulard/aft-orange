#!/usr/bin/env python3
"""Command Line Interface for the AFT API test client"""

import argparse
import json
import logging
import sys
from typing import Dict, List, Optional

from tools.test_client.client import AFTAPIClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("aft-api-client")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AFT API Test Client")
    parser.add_argument("--env", choices=["dev", "stage", "prod"], default="dev",
                        help="Environment to target")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create account command
    create_parser = subparsers.add_parser("create", help="Create a new AWS account")
    create_parser.add_argument("--input", required=True, help="Path to JSON file with account request data")
    
    # Update account command
    update_parser = subparsers.add_parser("update", help="Update an existing AWS account")
    update_parser.add_argument("account_name", help="Name of the account to update")
    update_parser.add_argument("--input", required=True, help="Path to JSON file with account request data")
    
    # Delete account command
    delete_parser = subparsers.add_parser("delete", help="Delete an AWS account")
    delete_parser.add_argument("account_name", help="Name of the account to delete")
    
    return parser.parse_args()


def load_json_file(file_path: str) -> Dict:
    """Load JSON data from a file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading JSON file: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the CLI"""
    args = parse_args()
    
    if not args.command:
        logger.error("No command specified. Use --help for usage information.")
        sys.exit(1)
    
    client = AFTAPIClient(environment=args.env)
    
    try:
        if args.command == "create":
            account_data = load_json_file(args.input)
            response = client.create_account(account_data)
            logger.info(f"Account creation request submitted: {response}")
            
        elif args.command == "update":
            account_data = load_json_file(args.input)
            response = client.update_account(args.account_name, account_data)
            logger.info(f"Account update request submitted: {response}")
            
        elif args.command == "delete":
            response = client.delete_account(args.account_name)
            logger.info(f"Account deletion request submitted: {response}")
            
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 