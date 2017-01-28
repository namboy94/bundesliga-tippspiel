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
 * @param $matchday int:                  The matchday to check
 * @return          array|mysqli_result:  The bets of the user for the specified matchday
 */
function getUserBets($matchday) {
    $db = new Database();

    return $db->query('SELECT bets.team_one, bets.team_two, bets.points, matches.id AS match_id '.
                      'FROM bets JOIN matches ON bets.match_id=matches.id WHERE matchday=?',
        'i', array($matchday), true, 'match_id');
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
