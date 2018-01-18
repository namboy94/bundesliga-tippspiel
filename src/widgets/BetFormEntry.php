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
use champlates\HtmlTemplate;
use cheetah\Bet;
use cheetah\Match;
use cheetah\Team;


/**
 * Class BetFormEntry
 * A Bet Form for a single match
 * @package bundesliga_tippspiel
 */
class BetFormEntry extends HtmlTemplate {

	/**
	 * BetFormEntry constructor.
	 * @param Match $match: The match to display
	 * @param Bet|null $bet: Optionally provides previous bet data
	 * @param bool $small: Indicates if this orm will be small or not
	 */
	public function __construct(
		Match $match, ? Bet $bet, bool $small = false) {

		parent::__construct(__DIR__ . "/templates/bet_form_entry.html", null);

		$disabled = $match->hasStarted() ? "disabled" : "";
		if ($bet !== null) {
			$homeDefault = (string)$bet->homeScore;
			$awayDefault = (string)$bet->awayScore;
		} else {
			$homeDefault = "";
			$awayDefault = "";
		}

		if ($small) {
			$inputSize = 2;
			$nameSize = 4;
			$homeName = $match->homeTeam->shortname;
			$awayName = $match->awayTeam->shortname;
		} else {
			$inputSize = 1;
			$nameSize = 5;
			$homeName = $match->homeTeam->name;
			$awayName = $match->awayTeam->name;
		}

		$this->bindParams([
			"HOME_ID" => $match->homeTeam->id,
			"AWAY_ID" => $match->awayTeam->id,
			"HOME_NAME" => $homeName,
			"AWAY_NAME" => $awayName,
			"HOME_ICON" => $match->homeTeam->icon,
			"AWAY_ICON" => $match->awayTeam->icon,
			"MATCH_ID" => $match->id,
			"DISABLED" => $disabled,
			"HOME_DEFAULT" => $homeDefault,
			"AWAY_DEFAULT" => $awayDefault,
			"INPUT_SIZE" => $inputSize,
			"NAME_SIZE" => $nameSize
		]);
	}
}
