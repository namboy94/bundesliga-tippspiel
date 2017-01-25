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
 * Class FullBetForm is class that models a Bet Form for a standalone bets page
 */
class FullBetForm extends HtmlGenerator {

    /**
     * @var array: The matches to be bet on
     */
    private $matches;

    /**
     * @var array: The teams represented by those bets
     */
    private $teams;

    /**
     * @var int:   The matchday to be bet on
     */
    private $matchday;

    /**
     * @var array|mysqli_result: The user's bets
     */
    private $userbets;

    /**
     * FullBetForm constructor.
     * @param int $matchday: The matchday to represent. Defaults to the current match day
     */
    public function __construct($matchday=-1) {

        $this->matches = ($matchday === -1 ? getCurrentMatches() : getMatches($matchday));
        $this->matchday = ($matchday === -1 ? getCurrentMatchDay() : $matchday);
        $this->teams = getTeams();
        $this->userbets = getUserBets($this->matchday);
        $_SESSION['current_matches'] = $this->matches;
        $_SESSION['current_teams'] = $this->teams;
        $_SESSION['current_bets'] = $this->userbets;

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

            if (isset($this->userbets[$match['id']])) {

                $bet = $this->userbets[$match['id']];
                $team_one_default = $bet['team_one'];
                $team_two_default = $bet['team_two'];

            }
            else {
                $team_one_default = null;
                $team_two_default = null;
            }

            $team_one_default = ($team_one_default === null ? 0 : $team_one_default);
            $team_two_default = ($team_two_default === null ? 0 : $team_two_default);

            $elements .= (new FullBetFormElement($team_one, $team_two, $team_one_default, $team_two_default))->render();
        }

        return str_replace('@ELEMENTS', $elements, $html);
    }
}

/**
 * Class FullBetFormElement is a class that models an entry in the full bet form
 */
class FullBetFormElement extends HtmlGenerator {

    /**
     * @var array: The home team of the matchup
     */
    private $team_one;

    /**
     * @var array: The away team of the matchup
     */
    private $team_two;

    /**
     * @var int: The default value to be displayed for the home team
     */
    private $team_one_default;

    /**
     * @var int: The default value to be displayed for the away team
     */
    private $team_two_default;

    /**
     * FullBetFormElement constructor.
     * @param $team_one         array: The home team
     * @param $team_two         array: The away team
     * @param $team_one_default int:   The default home team value
     * @param $team_two_default int:   The default away team value
     */
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

        if ($this->team_one_default !== null) {
            $html = str_replace('@DEFAULT_ONE', 'value="' . $this->team_one_default . '"', $html);
        }
        if ($this->team_two_default !== null) {
            $html = str_replace('@DEFAULT_TWO', 'value="' . $this->team_two_default . '"', $html);
        }

        return $html;
    }
}