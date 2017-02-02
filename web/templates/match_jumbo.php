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


class MatchJumbo extends HtmlGenerator {

    /**
     * @var array: The match to model in this jumbotron
     */
    private $match;

    private $team_one;
    private $team_two;

    /**
     * MatchJumbo constructor.
     * @param $match
     * @param $team_one
     * @param $team_two
     */
    public function __construct($match, $team_one, $team_two) {
        $this->match = $match;
        $this->team_one = $team_one;
        $this->team_two = $team_two;
        $this->template = dirname(__FILE__) . '/html/matchjumbo.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = $this->loadTemplate();

        $shortname_one = ($this->team_one['shortname'] !== ''
            ? $this->team_one['shortname'] : $this->team_one['name']);
        $shortname_two = ($this->team_two['shortname'] !== ''
            ? $this->team_two['shortname'] : $this->team_two['name']);

        $html = str_replace('@TEAM_ONE', $shortname_one, $html);
        $html = str_replace('@TEAM_TWO', $shortname_two, $html);

        return $html;
    }
}