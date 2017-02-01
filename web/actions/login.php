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
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();

$email = $_POST["login_email"];
$password = $_POST["login_password"];

$login_result = login($email, $password);

if (!$login_result['status']) {
    (new DismissableMessage('error', $login_result['title'], $login_result['body']))->show('../signup.php');
}
else {
    header('Location: ../index.php');
}
