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

include_once dirname(__FILE__) . '/../php/session.php';
include_once  dirname(__FILE__) . '/../php/registration.php';
include_once dirname(__FILE__) . '/../strings/dictionary.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];
$dictionary = new Dictionary($_SESSION['language']);


if ($email === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_EMAIL_TITLE',
        '@$REGISTER_ERROR_NO_EMAIL_BODY'))->show('../signup.php');
}
elseif (strlen($email) > 100) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_EMAIL_TOO_LONG_TITLE',
        '@$REGISTER_ERROR_EMAIL_TOO_LONG_BODY'))->show('../signup.php');
}
elseif ($username === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_USERNAME_TITLE',
        '@$REGISTER_ERROR_NO_USERNAME_BODY'))->show('../signup.php');
}
elseif (strlen($username) > 60) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_USERNAME_TOO_LONG_TITLE',
        '@$REGISTER_ERROR_USERNAME_TOO_LONG_BODY'))->show('../signup.php');
}
elseif (usernameExists($username)) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_USERNAME_EXISTS_TITLE',
        '@$REGISTER_ERROR_USERNAME_EXISTS_BODY'))->show('../signup.php');
}
elseif ($password === "") {
    (new DismissableMessage('error', '@$REGISTER_ERROR_NO_PASSWORD_TITLE',
        '@$REGISTER_ERROR_NO_PASSWORD_BODY'))->show('../signup.php');
}
elseif ($password != $repeat_password) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_PASSWORD_MISMATCH_TITLE',
        '@$REGISTER_ERROR_PASSWORD_MISMATCH_BODY'))->show('../signup.php');
}
elseif (strlen($password) < 8) {
    (new DismissableMessage('error', '@$REGISTER_ERROR_PASSWORD_TOO_SHORT_TITLE',
        '@$REGISTER_ERROR_PASSWORD_TOO_SHORT_BODY'))->show('../signup.php');
}
else {
    $registration = register($email, $username, $password, $_SERVER['REMOTE_ADDR']);

    if ($registration['status']) {

        $confirmation_token = $registration['token'];

        $headers = 'MIME-Version: 1.0' . "\r\n";
        $headers .= 'Content-type: text/html; charset=UTF-8' . "\r\n";
        $headers .= 'From: <noreply@tippspiel.krumreyh.com>';

        $title = $dictionary->translate('@$CONFIRMATION_EMAIL_TITLE');
        $body = $dictionary->translate('@$CONFIRMATION_EMAIL_BODY') . '<hr><a href="https://' . $_SERVER['SERVER_NAME']
            . '/actions/confirmation.php?confirmation=' . $confirmation_token . "&username=" . $username . '">'
            . $dictionary->translate('@$CONFIRMATION_EMAIL_LINK_NAME') . '<a>';

        mail($email, $title, $body, $headers);

        $message = new DismissableMessage('success', '@$REGISTER_SUCCESS_TITLE', '@$REGISTER_SUCCESS_BODY');
        $message->show('../signup.php');
    }

    else {
        $error_message = new DismissableMessage('error', $registration['error_title'], $registration['error_body']);
        $error_message->show('../signup.php');
    }
}
