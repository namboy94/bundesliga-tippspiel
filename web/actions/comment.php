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
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();

if (!isLoggedIn()) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_NOT_LOGGED_IN_TITLE',
        '@$COMMENT_ERROR_NOT_LOGGED_IN_BODY'))->show('../bets.php');
}
elseif (!isset($_POST['new_comment'])) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_NO_CONTENT_TITLE',
        '@$COMMENT_ERROR_NO_CONTENT_BODY'))->show('../bets.php');
}
else {

    $db = new Database();

    $user_id = $_SESSION['id'];
    $content = $_POST['new_comment'];
    $time = time();

    $comment_id = (int)$db->query('SELECT MAX(id) AS id FROM comments')->fetch_assoc()['id'] + 1;

    $db->queryWrite('INSERT INTO comments (id, user, created, last_modified, content) VALUES (?, ?, ?, ?, ?)',
        'iiiis', array($comment_id, $user_id, $time, $time, $content));

}

header('Location: ' . $_SERVER['HTTP_REFERER']);
