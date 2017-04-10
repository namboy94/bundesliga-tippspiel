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
include_once dirname(__FILE__) . '/../php/string_sanitize.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();
$db = new Database();

if (!isLoggedIn()) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_NOT_LOGGED_IN_TITLE',
        '@$COMMENT_ERROR_NOT_LOGGED_IN_BODY'))->show('../bets.php');
}
elseif (!isset($_POST['new_comment'])) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_NO_CONTENT_TITLE',
        '@$COMMENT_ERROR_NO_CONTENT_BODY'))->show('../bets.php');
}
elseif ($_POST['new_comment'] === '' || !hasVisibleContent($_POST['new_comment'])) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_EMPTY_TITLE',
        '@$COMMENT_ERROR_EMPTY_BODY'))->show('../bets.php');
}
elseif ($db->query('SELECT MAX(created) as created FROM comments WHERE user=?', 'i', array($_SESSION['id']))
        ->fetch_assoc()['created'] + 10 > time()) {
    (new DismissableMessage('error', '@$COMMENT_ERROR_RECENT_ACTIVITY_TITLE',
        '@$COMMENT_ERROR_RECENT_ACTIVITY_BODY'))->show('../bets.php');
}
else {
    $user_id = $_SESSION['id'];
    $content = sanitizeComment($_POST['new_comment']);

    if (strlen($content) > 255) {
        (new DismissableMessage('error', '@$COMMENT_ERROR_TOO_LONG_TITLE',
            '@$COMMENT_ERROR_TOO_LONG_BODY'))->show('../bets.php');
    }

    $time = time();
    $ip_address = $_SERVER["REMOTE_ADDR"];
    $comment_id = (int)$db->query('SELECT MAX(id) AS id FROM comments')->fetch_assoc()['id'] + 1;

    $db->queryWrite('INSERT INTO comments (id, user, created, last_modified, content, ip_address)
                     VALUES (?, ?, ?, ?, ?, ?)',
                    'iiiiss', array($comment_id, $user_id, $time, $time, $content, $ip_address));

}

header('Location: ' . $_SERVER['HTTP_REFERER']);
