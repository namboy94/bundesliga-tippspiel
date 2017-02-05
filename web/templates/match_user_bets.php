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
include_once dirname(__FILE__) . '/../php/database.php';

/**
 * Class MatchUserBets is a class that models a table of user bets for a specific match
 */
class MatchUserBets extends HtmlGenerator {

    /**
     * @var array: The match's bet data
     */
    private $bets;

    /**
     * MatchUserBets constructor.
     * @param $match_id int: The match ID
     */
    public function __construct($match_id) {
        $this->template = dirname(__FILE__) . '/html/match_user_bets_table.html';

        $db = new Database();
        $this->bets = $db->query('SELECT users.username AS username, bets.team_one AS team_one, 
                                  bets.team_two AS team_two, bets.points AS points FROM users LEFT JOIN bets 
                                  ON users.user_id=bets.user AND match_id=?',
            'i', array($match_id), true);
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    protected function render() {
        $html = $this->loadTemplate();

        $bets_html = '';
        foreach ($this->bets as $bet) {
            $bets_html .= (new MatchUserBet($bet))->render();
        }
        $html = str_replace('@ELEMENTS', $bets_html, $html);

        return $html;
    }
}

/**
 * Class MatchUserBet is a class that models a single entry in the match user bets table
 */
class MatchUserBet extends HtmlGenerator {

    /**
     * @var array: The specific bet to display
     */
    private $bet;

    /**
     * MatchUserBet constructor.
     * @param $bet array: The bet
     */
    public function __construct($bet) {
        $this->template = dirname(__FILE__) . '/html/match_user_bets_element.html';
        $this->bet = $bet;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    protected function render() {
        $html = $this->loadTemplate();
        $html = str_replace('@NAME', $this->bet['username'], $html);
        if ((int)$this->bet['points'] === -1 || (string)$this->bet['team_one'] == '' ||
            (string)$this->bet['team_one'] == '' || (string)$this->bet['points'] == '') {

            $html = str_replace('@POINTS', '-', $html);
            $html = str_replace('@TEAM_ONE', '-', $html);
            $html = str_replace('@TEAM_TWO', '-', $html);
        }
        else {
            $html = str_replace('@TEAM_ONE', $this->bet['team_one'], $html);
            $html = str_replace('@TEAM_TWO', $this->bet['team_two'], $html);
            $html = str_replace('@POINTS', $this->bet['points'], $html);
        }

        $points = (int)$this->bet['points'];
        switch ($points) {
            case 0: $html = str_replace('@LABELCLASS', 'danger', $html); break;
            case 1: $html = str_replace('@LABELCLASS', 'warning', $html); break;
            case 2: $html = str_replace('@LABELCLASS', 'default', $html); break;
            case 3: $html = str_replace('@LABELCLASS', 'info', $html); break;
            case 4: $html = str_replace('@LABELCLASS', 'primary', $html); break;
            case 5: $html = str_replace('@LABELCLASS', 'success', $html); break;
            default: $html = str_replace('@LABELCLASS', 'default', $html);
            }

        return $html;
    }
}