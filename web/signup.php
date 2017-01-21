<?php
/*  Copyright Hermann Krumrey <hermann@krumreyh.com> 2017

    This file is part of bundesliga-tippspiel.

    bundesliga-tippspiel is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    bundesliga-tippspiel is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
*/

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
        echo generate_success_message($dictionary['@$REGISTRATION_SUCCESS_TITLE'],
            $dictionary['@$REGISTRATION_SUCCESS_BODY']);
    }

    echo load_html("html_content/signup_body.html");
    echo load_html("html_content/templates/footer.html");

?>

</body>