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

Include "php_functions/auth.php";
Include "resources/strings-de.php";
Include "resources/strings-en.php";

session_start();

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];

switch ($_SESSION['language']) {
    case 'de':
        $dictionary = get_german_dictionary();
        break;
    default:
        $dictionary = get_english_dictionary();
}

if ($email === "") {
    header('Location: signup.php?no_email=true');
}
else if ($username === "") {
    header('Location: signup.php?no_username=true');
}
else if ($password === "") {
    header('Location: signup.php?no_password=true');
}
else if ($password != $repeat_password) {
    header('Location: signup.php?password_mismatch=true');
}
else if (username_exists($username)) {
    header('Location: signup.php?username_exists=true');
}
else if (email_used($email)) {
    header('Location: signup.php?email_used=true');
}
else if (strlen($password) < 8) {
    header('Location: signup.php?password_too_short=true');
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