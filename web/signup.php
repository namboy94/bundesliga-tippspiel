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

include_once 'php/gets.php';
include_once 'php/session.php';
include_once 'templates/form.php';
include_once 'templates/header.php';
include_once 'templates/navbar.php';
include_once 'strings/dictionary.php';

initializeSession();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$CONTACT_TITLE'))->echo();
echo '<body>';
generateDefaultHeaderNavbar('signup.php')->echo();
processDismissableMessages();

$signup_form = new Form('@$SIGNUP_SECTION_TITLE', 'actions/register.php', array(
    new FormTextEntry('@$REGISTER_EMAIL_TITLE', 'register_email', 'text',
        '@$REGISTER_EMAIL_PLACEHOLDER', 'reg_email'),
    new FormTextEntry('@$REGISTER_USERNAME_TITLE', 'register_username', 'text',
        '@$REGISTER_USERNAME_PLACEHOLDER', 'reg_username'),
    new FormTextEntry('@$REGISTER_PASSWORD_TITLE', 'register_password', 'password',
        '@$REGISTER_PASSWORD_PLACEHOLDER', 'reg_password'),
    new FormTextEntry('@$REGISTER_PASSWORD_REPEAT_TITLE', 'register_password_repeat', 'password',
        '@$REGISTER_PASSWORD_REPEAT_PLACEHOLDER', 'reg_password_repeat'),
    new ConfirmationButton('@$REGISTER_SUBMIT_TITLE')
));

$login_form = new Form('@$LOGIN_SECTION_TITLE', 'actions/login.php', array(
    new FormTextEntry('@$LOGIN_EMAIL_TITLE', 'login_email', 'text',
        '@$LOGIN_EMAIL_PLACEHOLDER', 'login_email_id'),
    new FormTextEntry('@$LOGIN_PASSWORD_TITLE', 'login_password', 'text',
        '@$LOGIN_PASSWORD_PLACEHOLDER', 'login_password_id'),
    new ConfirmationButton('@$LOGIN_SUBMIT_TITLE')
));

?>
<div class="container">
    <div class="jumbotron text-center">
        <h1><?php echo $dictionary->translate('@$SIGNUP_JUMBO') ?></h1>
    </div>
    <div class="row">
        <div class="col-sm-5 col-md-5 col-lg-5">
            <?php $signup_form->echo(); ?>
        </div>
        <div class="col-sm-2 col-md-2 col-lg-2">
            <hr width="1" size="500">
        </div>
        <div class="col-sm-5 col-md-5 col-lg-5">
            <?php $login_form->echo(); ?>
        </div>
    </div>
</div>
<?php



/*
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
    }*/

generateFooter('signup.php')->echoWithContainer();
echo '</body>';
