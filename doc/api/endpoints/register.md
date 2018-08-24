# /register

This API endpoint allows the registration of a new user.

##### Methods

* POST

##### Authorization

Not required

##### Parameters

* **username**: The username to register
* **email**: The email address to register
* **password**: The password to use
* **password_repeat**: The password again for verification purposes
* **recaptcha_response**: A valid Google ReCaptcha response using the site's site key

##### Response

{
    "status": "ok",
    "data": {
        "user_id": int,
        "confirm_key": str
    }
}

##### Notes

To complete the registration process, you will have to send a POST
request to the [confirm](confirm.md) endpoint using the user ID and
the confirmation key from the response.
