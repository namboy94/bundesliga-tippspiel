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
use cheetah\Match;


/**
 * Class Match
 * Page that displays information about a match
 * @package bundesliga_tippspiel
 */
class MatchPage extends Page {

	/**
	 * @var Match|null: The match to display
	 */
	private $match;

	/**
	 * Match constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{MATCH_TITLE}", "@{MATCH_JUMBO_TITLE}", "match.php", true
		);

		if ($this->match !== null) {
			/** @noinspection PhpUndefinedFieldInspection */
			$jumboTitle = $this->match->homeTeam->name .
				"<br>VS.<br>" . $this->match->awayTeam->name;

			$jumbotron = new DefaultJumbotron($jumboTitle);
			$this->addInnerTemplate("JUMBOTRON", $jumbotron);
		}
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 * @SuppressWarnings docBlocks
	 */
	protected function setContent(): array {

		$matchId = (int)$_GET["match_id"];
		$this->match = Match::fromId($this->db, $matchId);

		if ($this->match === null) {
			return [];
		} else {

			/** @noinspection PhpParamsInspection */
			$logoScore =
				new MatchLogoScoreHeader($this->dictionary, $this->match);
			/** @noinspection PhpParamsInspection */
			$matchGoals =
				new MatchGoalList($this->dictionary, $this->match);
			/** @noinspection PhpParamsInspection */
			$matchBets =
				new MatchBetlist($this->dictionary, $this->match, $this->user);

			return [$logoScore, $matchGoals, $matchBets];
		}
	}
}