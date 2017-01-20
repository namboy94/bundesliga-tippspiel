<?php
Include "php_functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("signup");
?>


<body>

<?php

    $dictionary = get_current_dictionary();

    echo load_navbar("signup");

    if (isset($_GET['password_mismatch'])) {
        echo generate_error_message($dictionary['@$PASSWORD_MISMATCH_TITLE'], $dictionary['@$PASSWORD_MISMATCH_BODY']);
    }
    else if (isset($_GET["no_email"])) {
        echo generate_error_message($dictionary['@$NO_EMAIL_TITLE'], $dictionary['@$NO_EMAIL_BODY']);
    }
    else if (isset($_GET["no_username"])) {
        echo generate_error_message($dictionary['@$NO_USERNAME_TITLE'], $dictionary['@$NO_USERNAME_BODY']);
    }
    else if (isset($_GET["no_password"])) {
        echo generate_error_message($dictionary['@$NO_PASSWORD_TITLE'], $dictionary['@$NO_PASSWORD_BODY']);
    }
    else if (isset($_GET["username_exists"])) {
        echo generate_error_message($dictionary['@$USERNAME_EXISTS_TITLE'], $dictionary['@$USERNAME_EXISTS_BODY']);
    }
    else if (isset($_GET["email_used"])) {
        echo generate_error_message($dictionary['@$EMAIL_USED_TITLE'], $dictionary['@$EMAIL_USED_BODY']);
    }
    else if (isset($_GET["password_too_short"])) {
        echo generate_error_message($dictionary['@$PASSWORD_TOO_SHORT_TITLE'],
                                    $dictionary['@$PASSWORD_TOO_SHORT_BODY']);
    }
    else if (isset($_GET["invalid_credentials"])) {
        echo generate_error_message($dictionary['@$INVALID_CREDENTIALS_TITLE'],
            $dictionary['@$INVALID_CREDENTIALS_BODY']);
    }
    else if (isset($_GET["not_existing_user"])) {
        echo generate_error_message($dictionary['@$NOT_EXISTING_USER_TITLE'],
            $dictionary['@$NOT_EXISTING_USER_BODY']);
    }
    else if (isset($_GET["confirmation_not_matching"])) {
        echo generate_error_message($dictionary['@$CONFIRMATION_NOT_MATCHING_TITLE'],
            $dictionary['@$CONFIRMATION_NOT_MATCHING_BODY']);
    }
    else if (isset($_GET["already_confirmed"])) {
        echo generate_error_message($dictionary['@$ALREADY_CONFIRMED_TITLE'],
            $dictionary['@$ALREADY_CONFIRMED_BODY']);
    }
    else if (isset($_GET["registration_initialized"])) {
        echo generate_success_message($dictionary['@$REGISTRATION_INITIALIZED_TITLE'],
            $dictionary['@$REGISTRATION_INITIALIZED_BODY']);
    }
    else if (isset($_GET["registration_success"])) {
        echo generate_success_message('@$REGISTRATION_SUCCESS_TITLE', '@$REGISTRATION_SUCCESS_BODY');
    }

    echo load_html("html_content/signup_body.html");
    echo load_html("html_content/templates/footer.html");

?>

</body>