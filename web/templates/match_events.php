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
 * Class MatchEvents is a class that models a match event table
 */
class MatchEvents extends HtmlGenerator {

    /**
     * @var array: The goals that have been scored so far
     */
    private $goals;

    /**
     * MatchEvents constructor.
     * @param $match_id int: The match's match ID
     */
    public function __construct($match_id) {
        $this->goals = getGoals($match_id);
        $this->template = dirname(__FILE__) . '/html/match_events.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    protected function render() {
        $html = $this->loadTemplate();

        $events = '';
        foreach($this->goals as $goal) {
            $events .=
                (new MatchEvent($goal['minute'], $goal['scorer'], $goal['team_one_score'], $goal['team_two_score']))
                    ->render();
        }

        return str_replace('@EVENTS', $events, $html);
    }
}

/**
 * Class GoalEvent is a class that models a Goal Event list item
 */
class GoalEvent extends HtmlGenerator {

    /**
     * @var int: The minute in which the event took place
     */
    public $minute;

    /**
     * @var int: The points of the home team after the event took place
     */
    private $team_one_score;

    /**
     * @var string: The name of the scorer
     */
    private $scorer;

    /**
     * @var int: The points of the away team after the event took place
     */
    private $team_two_score;

    /**
     * GoalEvent constructor.
     * @param $minute         int:    The minute of the event
     * @param $scorer         string: The scorer of the goal
     * @param $team_one_score int:    The home team's score
     * @param $team_two_score int:    The away team's score
     */
    public function __construct($minute, $scorer, $team_one_score, $team_two_score) {
        $this->minute = $minute;
        $this->scorer = $scorer;
        $this->team_one_score = $team_one_score;
        $this->team_two_score = $team_two_score;
        $this->template = dirname(__FILE__) . '/html/goal_event.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    protected function render() {
        $html = $this->loadTemplate();
        $html = str_replace('@MINUTE', $this->minute, $html);
        $html = str_replace('@SCORER', $this->scorer, $html);
        $html = str_replace('@TEAM_ONE_SCORE', $this->team_one_score, $html);
        $html = str_replace('@TEAM_TWO_SCORE', $this->team_two_score, $html);
        return $html;
    }
}
