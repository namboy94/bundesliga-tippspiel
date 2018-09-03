# /register

This API endpoint allows the registration of a new user.

##### Methods

* POST

##### Authorization

Not required

##### Parameters

* **username:str**: The username to register
* **email:str**: The email address to register
* **password:str**: The password to use
* **password-repeat:str**: The password again for verification purposes
* **g-recaptcha-response:str**: A valid Google ReCaptcha response using the site's site key


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
