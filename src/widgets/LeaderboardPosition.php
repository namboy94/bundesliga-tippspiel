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


/**
 * Class LeaderboardPosition
 * A Position in the LeaderboardTable
 * @package bundesliga_tippspiel
 */
class LeaderboardPosition extends HtmlTemplate {

	/**
	 * LeaderboardPosition constructor.
	 * @param int $position: The position of the user inside the table
	 * @param string $username: The name of the user
	 * @param int $points: The amount of points the user has
	 * @param string $colorClass: Which colour to display this user's entry in
	 */
	public function __construct(int $position,
								string $username,
								int $points,
								string $colorClass) {
		parent::__construct(
			__DIR__ . "/templates/leaderboard_position.html", null
		);
		$this->bindParams([
			"POSITION" => (string)$position,
			"USERNAME" => $username,
			"POINTS" => (string)$points,
			"COLORCLASS" => $colorClass
		]);
	}
}