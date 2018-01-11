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
use champlates\Dictionary;
use champlates\HtmlTemplate;
use cheetah\Match;
use cheetah\Team;


/**
 * Class MatchLogoScoreHeader
 * A Row that displays the Logos of both teams in a match as well as
 * the current score.
 * @package bundesliga_tippspiel
 */
class MatchLogoScoreHeader extends HtmlTemplate {

	/**
	 * MatchLogoScoreHeader constructor.
	 * @param Dictionary|null $dictionary: Dictionary used for translation
	 * @param Match $match: The match to display
	 */
	public function __construct(
		? Dictionary $dictionary, Match $match
	) {
		parent::__construct(
			__DIR__ . "/templates/match_logo_score_header.html", $dictionary
		);

		$this->bindParams([
			"HOME_ICON" => match_logo($match->homeTeam),
			"AWAY_ICON" => match_logo($match->awayTeam),
			"HOME_SCORE" => $match->homeFtScore,
			"AWAY_SCORE" => $match->awayFtScore
		]);
	}
}

function match_logo(Team $team): string {
	$path = "resources/images/emblems/" . $team->id . ".svg";
	if (!file_exists($path)) {
		$path = str_replace(".svg", ".png", $path);
	}
	return $path;
}