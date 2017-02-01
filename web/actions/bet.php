<?php

session_start();
include_once dirname(__FILE__) . '/../php/database.php';
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

$previous_bets = $_SESSION['current_bets'];
$teams = $_SESSION['current_teams'];
$matches = $_SESSION['current_matches'];
unset($_SESSION['current_matches']);
unset($_SESSION['current_teams']);
unset($_SESSION['current_bets']);

$db = new Database();

foreach($matches as $match) {

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
        echo 'NULL';
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