# authorize

Checks if an API key is valid for a given user.

## Input:

```json
    {
        "username": "VALUE",
        "api_key": "VALUE"
    }
```
    
## Response:

```json
    {
        "status": "success"
    }
```
    
    
or

```json
    {
        "status": "error",
        "cause": "unauthorized"
    }
```