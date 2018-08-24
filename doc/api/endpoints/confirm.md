# /confirm

This API endpoint allows the confirmation of a new user.

##### Methods

* POST

##### Authorization

Not required

##### Parameters

* **user_id**: The ID of the user to confirm
* **confirm_key**: The email address to register

##### Response

{
    "status": "ok",
    "data": {}
}

##### Notes

Users that should be confirmed must first be registered using the
[register](register.md) API endpoint.
