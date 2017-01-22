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

$username = $_GET['username'];
$confirmation_token = $_GET['confirmation'];

$status = confirm($username, $confirmation_token);

if ($status === "no_user") {
    header('Location: signup.php?not_existing_user=true');
}
elseif ($status === "no_match") {
    header('Location: signup.php?confirmation_not_matching=true');
}
elseif ($status === "already_confirmed") {
    header('Location: signup.php?already_confirmed=true');
}
elseif ($status === "success") {
    header('Location: signup.php?registration_success=true');
}


?>