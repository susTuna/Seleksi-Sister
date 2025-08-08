# Veritas Shield API Documentation

## Overview
Veritas Shield is a profanity detection service with customizable word lists. It provides a secure API using OAuth2 authentication to identify inappropriate content in text.

## Endpoints

### Register Application
```
/register
```

### Issue OAuth2 Token
```
/oauth/token
```

### Detect Bad Words
```
/detect
```

### Add/Remove Custom Word(s)
```
/custom-words
```

## Authentication
Authentication uses OAuth2 Client Credentials flow:
1. Register your application to receive credentials
2. Exchange credentials for an access token
3. Include the access token in all API requests

## Detailed API Reference

### 1. Register Application
**Endpoint:** `/register`  
**Method:** POST  
**Description:** Register a new application to use the API

**Request Body:**
```json
{
  "name": "YourAppName",
  "email": "your.email@example.com",
  "uri": "https://yourapp.com"
}
```

**Response:**
```json
{
  "message": "Application registered successfully",
  "client_id": "generated_client_id",
  "client_secret": "generated_client_secret"
}
```

### 2. Issue OAuth2 Token
**Endpoint:** `/oauth/token`  
**Method:** POST  
**Description:** Get an access token using client credentials

**Request Headers:**
- Content-Type: application/x-www-form-urlencoded
- Authorization: Basic base64(client_id:client_secret)

**Request Body:**
```
grant_type=client_credentials
```

**Response:**
```json
{
  "access_token": "token_value",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### 3. Detect Bad Words
**Endpoint:** `/detect`  
**Method:** POST  
**Description:** Check text for profanity/bad words

**Request Headers:**
- Content-Type: application/json
- Authorization: Bearer your_access_token

**Request Body:**
```json
{
  "text": "Text to check for bad words"
}
```

**Response (no profanity):**
```json
{
  "isProfane": false,
  "message": "No sensitive words detected"
}
```

**Response (profanity found):**
```json
{
  "isProfane": true,
  "detected_words": ["word1", "word2"]
}
```

### 4. Add/Remove Custom Words
**Endpoint:** `/custom-words`  
**Method:** POST  
**Description:** Customize the word detection by adding or removing words from whitelist or blacklist

**Request Headers:**
- Content-Type: application/json
- Authorization: Bearer your_access_token

**Request Body:**
```json
{
  "action": "add",
  "category": "blacklist",
  "words": ["word1", "word2", "word3"]
}
```

**Actions:** `add` or `remove`  
**Categories:** `blacklist` or `whitelist`

**Response:**
```json
{
  "success": true,
  "message": "Words successfully added to blacklist"
}
```

## Error Responses
All API errors return standard HTTP status codes with a JSON response:

```json
{
  "error": "error_code",
  "error_description": "Detailed error message"
}
```

### Common Error Codes
- 400: Bad Request - Invalid parameters or missing required fields
- 401: Unauthorized - Invalid or expired token
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server encountered an error

## Usage Example

### Python Example
```python
import requests
import base64
import json

# 1. Register your application (one-time setup)
register_response = requests.post(
    "https://api.veritasshield.com/register",
    json={
        "name": "MyContentFilter",
        "email": "developer@example.com"
    }
)
client_data = register_response.json()
client_id = client_data["client_id"]
client_secret = client_data["client_secret"]

# 2. Get OAuth token
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
token_response = requests.post(
    "https://api.veritasshield.com/oauth/token",
    headers={"Authorization": f"Basic {encoded_credentials}"},
    data={"grant_type": "client_credentials"}
)
token = token_response.json()["access_token"]

# 3. Detect bad words
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
detect_response = requests.post(
    "https://api.veritasshield.com/detect",
    headers=headers,
    json={"text": "Check this text for profanity"}
)
result = detect_response.json()
print(result)
```

## Support
For questions or support, please contact support@veritasshield.com
