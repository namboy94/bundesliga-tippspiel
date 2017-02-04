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
    $result = $db->query('SELECT MIN(matchday) as matchday FROM matches WHERE finished=FALSE');
    return (int) $result->fetch_assoc()['matchday'];
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
 * @param $matchday int:                   The matchday to check
 * @param $user     int:                   The user for which to fetch the bets
 * @return          array|mysqli_result :  The bets of the user for the specified matchday
 */
function getUserBets($matchday, $user) {
    $db = new Database();

    return $db->query('SELECT bets.team_one, bets.team_two, bets.points, matches.id AS match_id '.
                      'FROM bets JOIN matches ON bets.match_id=matches.id WHERE matchday=? AND user=?',
        'ii', array($matchday, $user), true, 'match_id');
}

/**
 * Calculates the current leaderboard
 * @return array the leaderboard as a multi-dimensional array. The array will be sorted by points in a descending order
 *          [{username, user_id, points}]
 */
function getLeaderboard() {
    $db = new Database();

    $users = $db->query('SELECT user_id, username FROM users', '', array(), true, 'user_id');
    $leaderboard = $db->query('SELECT * FROM leaderboard ORDER BY points DESC', '', array(), true, 'user_id');

    foreach($leaderboard as $user_id => $entry) {
        $leaderboard[$user_id]['username'] = $users[$user_id]['username'];
    }

    return $leaderboard;

}

/**
 * Retrieves a specific Match from the database
 * @param $match_id int:        The match ID to search for
 * @return          null|array: The match, or null if none was found
 */
function getMatch($match_id) {
    $db = new Database();

    $result = $db->query('SELECT * FROM matches WHERE id=?', 's', array($match_id), true);
    if (count($result) !== 1) {
        return null;
    }
    else {
        return $result[0];
    }
}

/**
 * Retrieves the teams in a particular match
 * @param $match array: The match for which to retrieve the teams for
 * @return       array: The two team, first the home team then then away team
 */
function getTeamsForMatch($match) {
    $db = new Database();

    $team_one = $db->query('SELECT * FROM teams WHERE id=?', 's', array($match['team_one']));
    $team_two = $db->query('SELECT * FROM teams WHERE id=?', 's', array($match['team_two']));

    return array('team_one' => $team_one->fetch_assoc(), 'team_two' => $team_two->fetch_assoc());

}

/**
 * Checks if a match has already started
 * @param $match array:   The match to check
 * @return       boolean: True if the match has started, else false
 */
function hasMatchStarted($match) {
    $start_time = strtotime($match['matchtime']);
    $current_time = time();
    return $current_time > $start_time;
}

/**
 * Fetches data about the current score of a match
 * @param $match_id int:   The match id to check for
 * @return          array: The current scores in an array
 */
function getCurrentScore($match_id) {
    $db = new Database();
    return $db->query('SELECT MAX(minute), team_one_score, team_two_score FROM goals WHERE match_id=?',
        'i', array($match_id), true);
}