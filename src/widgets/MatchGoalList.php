<?php
/**
 * Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>
 *
 * This file is part of bundesliga-tippspiel.
 *
 * bundesliga-tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga-tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga-tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use cheetah\Goal;
use cheetah\Match;


/**
 * Class MatchGoalList
 * Displays the goals that fell in a match
 * @package bundesliga_tippspiel
 */
class MatchGoalList extends HtmlTemplate {

	/**
	 * MatchGoalList constructor.
	 * @param Dictionary|null $dictionary: Dictionary used to translate
	 * @param Match $match: The match from which to display the goals
	 */
	public function __construct(
		? Dictionary $dictionary, Match $match
	) {
		$db = Functions::getMysqli();
		$goals = Goal::getFromMatchId($db, $match->id);
		$db->close();

		$goalEntries = [];
		foreach ($goals as $goal) {

			$goalEntry = new HtmlTemplate(
				__DIR__ . "/templates/match_goal.html", $dictionary
			);
			$goalEntry->bindParams([
				"GOAL_MINUTE" => $goal->minute,
				"GOAL_HOME_SCORE" => $goal->homeScore,
				"GOAL_AWAY_SCORE" => $goal->awayScore,
				"GOAL_SCORER" => $goal->player->name
			]);

			array_push($goalEntries, $goalEntry);
		}

		parent::__construct(
			__DIR__ . "/templates/match_goal_list.html", $dictionary
		);

		$this->bindParams([
			"HOME_NAME_TITLE" => $match->homeTeam->abbreviation,
			"AWAY_NAME_TITLE" => $match->awayTeam->abbreviation
		]);
		$this->addCollectionFromArray("GOALS", $goalEntries);

	}


}