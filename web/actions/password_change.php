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
include_once dirname(__FILE__) . '/../php/registration.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

session_start();

$email = $_SESSION['userdata']['email'];

$current = $_POST['current'];
$new = $_POST['new'];
$repeat = $_POST['repeat'];


if (!passwordMatches($email, $current)) {
    (new DismissableMessage('error', '@$PASSWORD_CHANGE_CURRENT_WRONG_TITLE', '@$PASSWORD_CHANGE_CURRENT_WRONG_BODY'))
        ->show('../profile.php');
}
elseif (!strlen($new) >= 8) {
    (new DismissableMessage('error', '@$PASSWORD_CHANGE_TOO_SHORT_TITLE', '@$PASSWORD_CHANGE_TOO_SHORT_BODY'))
        ->show('../profile.php');
}
elseif ($new !== $repeat) {
    (new DismissableMessage('error', '@$PASSWORD_CHANGE_MISMATCH_TITLE', '@$PASSWORD_CHANGE_MISMATCH_BODY'))
        ->show('../profile.php');
}
else {
    changePassword($email, $new);
    (new DismissableMessage('success', '@$PASSWORD_CHANGE_SUCCESS_TITLE', '@$PASSWORD_CHANGE_SUCCESS_BODY'))
        ->show('../profile.php');
}