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

include_once dirname(__FILE__) . '/../php/matchdb.php';
include_once dirname(__FILE__) . '/../php/session.php';
include_once dirname(__FILE__) . '/../php/database.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

initializeSession();
redirectInvalidUser('../index.html');

$previous_bets = $_SESSION['current_bets'];
$teams = $_SESSION['current_teams'];
$matches = $_SESSION['current_matches'];
unset($_SESSION['current_matches']);
unset($_SESSION['current_teams']);
unset($_SESSION['current_bets']);

$db = new Database();

foreach($matches as $match) {

    if (hasMatchStarted($match)) {
        continue;
    }

    $team_one = $_POST[$match['team_one']];
    $team_two = $_POST[$match['team_two']];

    if ($team_one < 0 || $team_two < 0) {
        (new DismissableMessage('error', '@$INVALID_BET_VALUE_NEGATIVE_NUMBER_TITLE',
            '@$INVALID_BET_VALUE_NEGATIVE_NUMBER_BODY'))->show('../bets.php');
    }
    if ($team_one > 1000 || $team_two > 1000) {
        (new DismissableMessage('error', '@$INVALID_BET_VALUE_TOO_HIGH_TITLE',
            '@$INVALID_BET_VALUE_TOO_HIGH_BODY'))->show('../bets.php');
    }
    if ($_POST[$match['team_one']] == null || $_POST[$match['team_two']] == null) {
        continue;
    }
    if (!is_int($_POST[$match['team_one']]) || !is_int($_POST[$match['team_two']])) {
        continue;
    }

    if (isset($previous_bets[$match['id']])) {
        $args = array($_POST[$match['team_one']], $_POST[$match['team_two']], $_SESSION['id'], $match['id']);
        $db->queryWrite('UPDATE bets SET team_one=?, team_two=? WHERE user=? AND match_id=?', 'iiii', $args);
    }
    else {
        $args = array($_SESSION['id'], $match['id'], $_POST[$match['team_one']], $_POST[$match['team_two']], -1);
        $db->queryWrite('INSERT INTO bets (user, match_id, team_one, team_two, points) VALUES (?, ?, ?, ?, ?)',
            'iiiii', $args);
    }

}

(new DismissableMessage('success', '@$BETS_UPDATED_TITLE', '@$BETS_UPDATED_BODY'))->show('../bets.php');
