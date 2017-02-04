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

include_once dirname(__FILE__) . '/generator.php';
include_once dirname(__FILE__) . '/../php/matchdb.php';


/**
 * Class LeadboardTable is a class that models the leaderboard table
 */
class LeaderboardTable extends HtmlGenerator {

    /**
     * @var string: The username of the current user
     */
    private $username;

    /**
     * LeadboardTable constructor.
     * @param $username string: The username to highlight on the table
     */
    public function __construct($username) {
        $this->template = dirname(__FILE__) . '/html/leaderboard.html';
        $this->username = $username;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = $this->loadTemplate();

        $leaderboard = getLeaderboard();

        $elements = '';
        $position = 1;
        foreach($leaderboard as $user) {
            $elements .=
                (new LeaderboardUser($position, $user['username'], $user['points'], $this->username))->render();
            $position += 1;
        }

        return str_replace('@ELEMENTS', $elements, $html);
    }
}

/**
 * Class LeaderboardUser is the class that models an entry in the leaderboard table
 */
class LeaderboardUser extends HtmlGenerator {

    /**
     * @var int: The position of the table entry
     */
    private $position;

    /**
     * @var string: The username to be displayed on the table entry
     */
    private $username;

    /**
     * @var int: The points the user currently has
     */
    private $points;

    /**
     * LeaderboardUser constructor.
     * @param $position    int:    The position of the entry
     * @param $username    string: The username of the entry
     * @param $points      int:    The points of the entry
     * @param $active_user string: The currently active user, which defines if this entry is selected or not
     */
    public function __construct($position, $username, $points, $active_user) {
        $this->position = $position;
        $this->username = $username;
        $this->points = $points;

        $this->template = dirname(__FILE__) .
            ($username === $active_user ? '/html/leaderboard_active_user.html' : '/html/leaderboard_user.html');
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = $this->loadTemplate();
        $html = str_replace('@POSITION', $this->position, $html);
        $html = str_replace('@USERNAME', $this->username, $html);
        $html = str_replace('@POINTS', $this->points, $html);
        return $html;
    }
}