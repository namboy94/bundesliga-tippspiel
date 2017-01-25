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

include_once dirname(__FILE__) . '/database.php';


/**
 * Fetches the current Match Day
 * @return array: Array of match arrays
 */
function getCurrentMatches() {
    return getMatches(getCurrentMatchday());
}

/**
 * Determines the current match day number
 * @return int: The current matchday
 */
function getCurrentMatchday() {
    $db = new Database();
    $result = $db->query('SELECT MAX(matchday) as matchday FROM matches WHERE city != "Unknown"', '', array());
    $matchday = $result->fetch_assoc()['matchday'] + 1;
    return $matchday;
}

/**
 * Fetches a given match day
 * @param $matchday int:   The match day to fetch
 * @return          array: The match arrays
 */
function getMatches($matchday) {
    $db = new Database();
    return $db->query('SELECT * FROM matches WHERE matchday=?', 'i', array($matchday), true);
}

/**
 * @return array: All teams in the teams table of the database
 */
function getTeams() {
    $db = new Database();
    $result = $db->query('SELECT * FROM teams', '', array());
    $teams = array();
    while($team = $result->fetch_assoc()) {
        $teams[$team['id']] = $team;
    }
    return $teams;
}

/**
 * @param $matchday int:                  The matchday to check
 * @return          array|mysqli_result:  The bets of the user for the specified matchday
 */
function getUserBets($matchday) {
    $db = new Database();
    return $db->query('SELECT bets.team_one, bets.team_two, bets.locked, matches.id AS match_id ' .
                         'FROM bets JOIN matches ON bets.match_id = matches.id WHERE matchday=?',
        'i', array($matchday), true, 'match_id');
}


function getLeaderboard() {
    $db = new Database();

    $bets = $db->query('SELECT user, match_id, team_one, team_two FROM bets', '', array(), true);
    $users = $db->query('SELECT user_id FROM users', '', array(), true);
    $matches = $db->query('SELECT id, team_one_ft, team_two_ft FROM matches', '', array(), true);

    $userpoints = array();
    foreach($users as $user) {
        $userpoints[$user['user_id']] = 0;
    }

    foreach($matches as $match) {
        $team_one = $match['team_one_ft'];
        $team_two = $match['team_two_ft'];

        if ((int) $team_one === -1 || (int) $team_two === -1) {
            continue;
        }

        foreach($userpoints as $user => $points) {

            foreach ($bets as $bet) {

                if (((int) $bet['user'] === (int) $user) && ((int) $bet['match_id'] === (int) $match['id'])) {
                    $userpoints[$user] += calculatePoints($bet['team_one'], $bet['team_two'], $team_one, $team_two);
                }
            }
        }
    }

    return $userpoints;
}

function calculatePoints($team_one_bet, $team_two_bet, $team_one_actual, $team_two_actual) {

    $points = 0;
    if ($team_one_actual === $team_one_bet) {
        $points += 1;  // Check if first team score was tipped correctly
    }
    if ($team_two_actual === $team_two_bet) {
        $points += 1;  // Check if second team score was tipped correctly
    }
    if (($team_one_bet - $team_two_bet) === ($team_one_actual - $team_two_actual)) {
        $points += 1;  // Check if goal difference was tipped correctly
    }
    if ((($team_one_bet > $team_two_bet) === ($team_one_actual > $team_two_actual)) &&
        (($team_one_bet === $team_two_bet) === ($team_one_actual === $team_two_actual))) {
        $points += 1;  // Check if tendency was tipped correctly
    }
    if ($points === 4) {
        $points += 1;  // Extra point for placing a correct bet
    }
    return $points;

}