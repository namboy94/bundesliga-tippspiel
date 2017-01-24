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


class FullBetForm extends HtmlGenerator {

    private $matches;
    private $teams;
    private $matchday;
    private $userbets;

    public function __construct($matchday=-1) {

        $this->matches = ($matchday === -1 ? getCurrentMatches() : getMatches($matchday));
        $this->matchday = ($matchday === -1 ? getCurrentMatchDay() : $matchday);
        $this->teams = getTeams();

    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {

        $html = file_get_contents(dirname(__FILE__) . '/html/betform_full.html');
        $title = '@$BUNDESLIGA_MATCHDAY_BETS_TITLE ' . $this->matchday;

        $html = str_replace('@TITLE', $title, $html);
        $html = str_replace('@SUBMIT', '@$BET_SUBMIT_BUTTON_TEXT', $html);

        $elements = '';
        foreach ($this->matches as $match) {
            $team_one = $this->teams[$match['team_one']];
            $team_two = $this->teams[$match['team_two']];
            $elements .= (new FullBetFormElement($team_one, $team_two))->render();
        }

        return str_replace('@ELEMENTS', $elements, $html);
    }
}

class FullBetFormElement extends HtmlGenerator {

    private $team_one;
    private $team_two;
    private $team_one_default;
    private $team_two_default;

    public function __construct($team_one, $team_two, $team_one_default, $team_two_default) {
        $this->team_one = $team_one;
        $this->team_two = $team_two;
        $this->team_one_default = $team_one_default;
        $this->team_two_default = $team_two_default;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents(dirname(__FILE__) . '/html/betform_full_element.html');

        $html = str_replace('@TEAM_ONE', $this->team_one['name'], $html);
        $html = str_replace('@TEAM_TWO', $this->team_two['name'], $html);
        $html = str_replace('@NAME_ONE', $this->team_one['id'], $html);
        $html = str_replace('@NAME_TWO', $this->team_two['id'], $html);
        $html = str_replace('@DEFAULT_ONE', $this->team_one_default, $html);
        $html = str_replace('@DEFAULT_TWO', $this->team_two_default, $html);

        return $html;
    }
}