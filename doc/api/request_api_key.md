# request_api_key

Requests an API key for a given username and password.
Will delete the existing API key.

## Input:

```json
    {
        "username": "VALUE",
        "password": "VALUE"
    }
```
    
## Response:

```json
    {
        "status": "success",
        "key": "VALUE"   
    }
```