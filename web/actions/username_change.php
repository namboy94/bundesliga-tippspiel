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
include_once dirname(__FILE__) . '/../php/database.php';
include_once dirname(__FILE__) . '/../php/registration.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();
redirectInvalidUser('../index.html');

$user_id = $_SESSION['id'];
$new_name = $_POST['new_name'];

$db = new Database();

if (usernameExists($new_name)) {
    (new DismissableMessage('error', '@$USERNAME_CHANGE_NAME_TAKEN_TITLE', '@$USERNAME_CHANGE_NAME_TAKEN_BODY'))
        ->show('../profile.php');
}
elseif ($new_name === "") {
    (new DismissableMessage('error', '@$USERNAME_CHANGE_EMPTY_TITLE',
        '@$USERNAME_CHANGE_EMPTY_BODY'))->show('../profile.php');
}
elseif (strlen($new_name) > 60) {
    (new DismissableMessage('error', '@$USERNAME_CHANGE_TOO_LONG_TITLE',
        '@$USERNAME_CHANGE_TOO_LONG_BODY'))->show('../profile.php');
}
else {
    $_SESSION['userdata']['name'] = $new_name;
    $db->queryWrite('UPDATE users SET username=? WHERE user_id=?', 'si', array($new_name, $user_id));
    (new DismissableMessage('success', '@$USERNAME_CHANGE_SUCCESS_TITLE',
        '@$USERNAME_CHANGE_SUCCESS_BODY'))->show('../profile.php');
}