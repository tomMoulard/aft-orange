# AWS Account Factory for Terraform (AFT) API

An API Gateway integration for automating AWS account provisioning and management via Account Factory for Terraform (AFT).

## Project Overview

This project implements an AWS API Gateway that handles events to create and manage AWS accounts using AFT (Account Factory for Terraform). The solution leverages Lambda functions to process API requests, generate the necessary configuration files, and commit them to a private GitLab repository.

## Architecture

- **API Gateway**: Exposes endpoints to trigger account creation and management operations
- **Lambda Functions**: Process requests, generate configuration files, and interact with GitLab
- **GitLab Integration**: Stores AFT configuration files in a dedicated repository structure
- **AWS AFT**: Provisions and configures new AWS accounts based on the GitLab repository content

## Workflow

1. Client sends a request to the API Gateway
2. API Gateway triggers the appropriate Lambda function
3. Lambda generates the required configuration files based on the request parameters, using templated configuration.
4. Lambda commits and pushes the files to the designated GitLab repository
5. AFT detects the new configuration and provisions/updates the AWS account accordingly

## Implementation Status

- [x] Set up basic project structure and dependencies
- [x] Define data models for account requests using Pydantic
- [x] Implement factory pattern for generating account configurations
- [x] Create GitLab client for repository operations
- [x] Implement account validation logic
- [x] Create a test client to call the API Gateway
- [x] Define basic unit and integration tests
- [x] Create templates for AFT configuration files
- [x] Set up API Gateway endpoints for account operations (create, update, delete, upgrade, downgrade, add and remove options) using terraform
- [x] Implement authentication and authorization for the API
- [x] Configure error handling and logging
- [x] Set up CI/CD pipeline for deployment using gitlab-ci
- [ ] Set up monitoring and alerting

## Development

### Prerequisites

- AWS Account with AFT configured
- GitLab repository for AFT configurations
- AWS CLI configured locally
- Terraform CLI
- Python 3.9+

### Getting Started

1. Clone the repository
2. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```
3. Set up required environment variables:
   ```
   export GITLAB_URL=https://gitlab.example.com
   export GITLAB_TOKEN=your-gitlab-token
   export GITLAB_PROJECT_ID=12345
   export GITLAB_BRANCH=main
   ```
4. Run tests:
   ```
   pytest
   ```

### Using the Test Client

The project includes a test client to interact with the API:

```bash
# Create an account
python -m tools.test_client.cli create --input tools/test_client/samples/create_account.json

# Update an account
python -m tools.test_client.cli update accountname --input tools/test_client/samples/create_account.json

# Delete an account
python -m tools.test_client.cli delete accountname
```

## Security Considerations

- API Gateway implements Cognito-based JWT authentication and role-based authorization
- GitLab repository access should be restricted and authenticated
- AWS account provisioning should follow least privilege principle
- Sensitive data should be stored securely using AWS Secrets Manager or Parameter Store

## Authentication and Authorization

The API uses AWS Cognito for authentication and a Lambda authorizer for authorization:

- **Authentication**: AWS Cognito User Pools with JWT tokens
- **Authorization**: Lambda authorizer that validates JWT tokens and checks permissions
- **User Groups**:
  - Administrators: Have full access to create, update, and delete accounts
  - Readers: Have read-only access to account information

To call the API, clients must:
1. Authenticate with Cognito to get a JWT token
2. Include the token in the Authorization header: `Authorization: Bearer <token>`

## Best Practices

- Use AWS CloudFormation or Terraform to deploy the infrastructure as code
- Follow factory pattern for creating account configurations
- Implement proper error wrapping when returning errors
- Use concise, focused implementations