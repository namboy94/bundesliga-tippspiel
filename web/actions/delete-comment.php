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
redirectInvalidUser('../index.php');

if (!isset($_GET['comment'])) {
    (new DismissableMessage('error', '@$BET_DELETE_FAILED_NO_COMMENT_TITLE',
        '@$BET_DELETE_FAILED_NO_COMMENT_BODY'))->show('../index.php');
}
else {
    $db = new Database();
    //$db->queryWrite('UPDATE comments SET content=?, user=?, last_modified=? WHERE user=? AND id=?', 'siiii',
    //    array('@$DELETED_COMMENT_MESSAGE', -1, time(), $_SESSION['id'], (int)$_GET['comment']));
    $db->queryWrite('DELETE FROM comments WHERE user=? AND id=?', 'ii', array($_SESSION['id'], (int)$_GET['comment']));
    header('Location: ' . $_SERVER['HTTP_REFERER']);
    exit();
}