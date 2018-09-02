# /rapi_key

This API endpoint allows the acquisition of a new API key.
This API key may be used to access API endpoints that require
authorization by using HTTP basic authentication.

Additionally, an API may be revoked using the DELETE method on this endpoint.

##### Methods

* POST
* DELETE

##### Authorization

Not required

##### Parameters

POST:

* **username**: The username of the user
* **password**: The password of the user


    {
        "username": str,
        "password": str
    }
    
DELETE:

* **api_key**: The previously generated API key


    {
        "api_key": str
    }

##### Response

POST:

* **api_key**: The generated API key
* **expiration**: The expiration timestamp as a UTC UNIX timestamp

    {
        "status": "ok",
        "data": {
            "api_key": str,
            "expiration": int
        }
    }

DELETE:

    {
        "status": "ok",
        "data": {}
    }