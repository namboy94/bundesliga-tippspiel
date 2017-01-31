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

include_once dirname(__FILE__) . '/../php/registration.php';
include_once dirname(__FILE__) . '/../strings/dictionary.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

session_start();
$dictionary = new Dictionary($_SESSION['language']);

$email = $_POST['reset_email'];
$temporary_password = resetPassword($email);

if ($temporary_password !== null) {

    $headers = 'MIME-Version: 1.0' . "\r\n";
    $headers .= 'Content-type: text/html; charset=UTF-8' . "\r\n";
    $headers .= 'From: <noreply@tippspiel.krumreyh.com>';

    $body = $dictionary->translate('@$PASSWORD_RESET_EMAIL_BODY');
    $body = str_replace('@TEMPORARY_PASSWORD', $temporary_password, $body);

    mail($email, $dictionary->translate('@$PASSWORD_RESET_EMAIL_SUBJECT'), $body, $headers);

}

(new DismissableMessage('info', '@$PASSWORD_RESET_DISMISSABLE_TITLE', '@$PASSWORD_RESET_DISMISSABLE_BODY'))
    ->show('../signup.php');
