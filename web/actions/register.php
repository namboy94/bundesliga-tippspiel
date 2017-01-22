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

session_start();

include_once dirname(__FILE__) . '/../strings/dictionary.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];
$dictionary = new Dictionary($_SESSION['language']);


if ($email === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_EMAIL_TITLE',
        '@$REGISTER_ERROR_NO_EMAIL_BODY'))->show('../signup.php');
}
else if ($username === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_USERNAME_TITLE',
        '@$REGISTER_ERROR_NO_USERNAME_BODY'))->show('../signup.php');
}
else if ($password === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_PASSWORD_TITLE',
        '@$REGISTER_ERROR_NO_PASSWORD_BODY'))->show('../signup.php');
}
else if ($password != $repeat_password) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_PASSWORD_MISSMATCH_TITLE',
        '@$REGISTER_ERROR_PASSWORD_MISSMATCH_BODY'))->show('../signup.php');
}
else if (username_exists($username)) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_USERNAME_EXISTS_TITLE',
        '@$REGISTER_ERROR_USERNAME_EXISTS_BODY'))->show('../signup.php');
}
else if (email_used($email)) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_EMAIL_USED_TITLE',
        '@$REGISTER_ERROR_EMAIL_USED_BODY'))->show('../signup.php');
}
else if (strlen($password) < 8) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_PASSWORD_TOO_SHORT_TITLE',
        '@$REGISTER_ERROR_PASSWORD_TOO_SHORT_BODY'))->show('../signup.php');
}
else {

    $confirmation = create_new_user($email, $username, $password);

    $from = "From: " . $dictionary['@$WEBSITE_NAME']  . "<noreply@tippspiel.krumreyh.com>";
    $title = $dictionary['@$CONFIRMATION_NAME'];
    $body = $dictionary['@$EMAIL_CONFIRMATION'] . '<a href="tippspiel.krumreyh.com/confirmation.php?confirmation='
            . $confirmation . "&username=" . $username . '">Confirmation<a>';
    mail($email, $title, $body, $from);

    header('Location: signup.php?registration_initialized=true');

}



?>