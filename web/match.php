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

include_once 'php/gets.php';
include_once 'php/session.php';
include_once 'php/matchdb.php';
include_once 'templates/form.php';
include_once 'templates/navbar.php';
include_once 'templates/header.php';
include_once 'templates/betform.php';
include_once 'strings/dictionary.php';
include_once 'templates/title_jumbotron.php';
include_once 'templates/dismissable_message.php';

initializeSession();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

$match = 0;
if (isset($_POST['match_id'])) {
    $match = getMatch($_POST['match_id']);
}
if ($match === null) {
    (new DismissableMessage('error', '@$MATCH_NOT_FOUND_ERROR_TITLE', '@$MATCH_NOT_FOUND_ERROR_BODY'))
        ->show('index.html');
}

(new Header('@$MATCH_TITLE'))->echo();
processDismissableMessages();