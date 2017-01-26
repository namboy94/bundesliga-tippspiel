
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


class LeadboardTable extends HtmlGenerator {

    private $username;

    public function __construct($username) {
        $this->template = dirname(__FILE__) . '/html/leaderboard.html';
        $this->username = $username;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents($this->template);

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

class LeaderboardUser extends HtmlGenerator {

    private $position;
    private $username;
    private $points;

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
        $html = file_get_contents($this->template);
        $html = str_replace('@POSITION', $this->position, $html);
        $html = str_replace('@USERNAME', $this->username, $html);
        $html = str_replace('@POINTS', $this->points, $html);
        return $html;
    }
}