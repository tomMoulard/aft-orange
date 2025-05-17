# AFT API Documentation

## Overview

The AFT API allows you to create, update, and delete AWS accounts through Account Factory for Terraform (AFT).

## Base URL

- Development: `https://api-dev.example.com`
- Staging: `https://api-stage.example.com`
- Production: `https://api-prod.example.com`

## Authentication

All API requests require authentication. Authentication is handled through API keys that should be included in the `Authorization` header.

```
Authorization: Bearer <api-key>
```

## Endpoints

### Create Account

**Endpoint:** `POST /accounts`

Creates a new AWS account through AFT.

**Request Body:**

```json
{
  "account_name": "string",
  "email": "string",
  "organizational_unit": "string",
  "account_tags": {
    "key1": "string",
    "key2": "string"
  },
  "custom_fields": {
    "key1": "string",
    "key2": "string"
  },
  "sso_user_email": "string",
  "sso_user_first_name": "string",
  "sso_user_last_name": "string"
}
```

**Required Fields:**
- `account_name`: Alphanumeric name for the account
- `email`: Email address for the AWS account
- `organizational_unit`: OU where the account will be placed

**Optional Fields:**
- `account_tags`: Tags to apply to the account
- `custom_fields`: Custom fields for account configuration
- `sso_user_email`: Email for SSO user access
- `sso_user_first_name`: First name for SSO user
- `sso_user_last_name`: Last name for SSO user

**Response:**

```json
{
  "message": "Account creation request submitted",
  "account_name": "string",
  "commit_sha": "string"
}
```

### Update Account

**Endpoint:** `PUT /accounts/{account_name}`

Updates an existing AWS account.

**Request Body:**

Same as Create Account.

**Response:**

```json
{
  "message": "Account update request submitted",
  "account_name": "string",
  "commit_sha": "string"
}
```

### Delete Account

**Endpoint:** `DELETE /accounts/{account_name}`

Deletes an existing AWS account.

**Request Body:**

```json
{
  "account_name": "string"
}
```

**Response:**

```json
{
  "message": "Account deletion request submitted",
  "account_name": "string",
  "commit_sha": "string"
}
```

## Error Responses

All endpoints return a standard error format:

```json
{
  "error": "Error message description"
}
```

**Common Status Codes:**

- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Rate Limits

API requests are limited to 100 requests per minute per API key. 