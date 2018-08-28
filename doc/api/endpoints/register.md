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
* **password-repeat**: The password again for verification purposes
* **g-recaptcha-response**: A valid Google ReCaptcha response using the site's site key


    {
        "username": str,
        "email": str,
        "password": str,
        "password-repeat": str,
        "g-recaptcha-response": str
    }

##### Response

    {
        "status": "ok",
        "data": {}
    }

##### Notes

To complete the registration process, the user will have to visit the URL in
the confirmation email.
