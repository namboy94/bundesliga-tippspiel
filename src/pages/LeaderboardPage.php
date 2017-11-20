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


/**
 * Class Leaderboard
 * Models a Leaderboard of all users
 * @package bundesliga_tippspiel
 */
class LeaderboardPage extends Page {

	/**
	 * Leaderboard constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{LEADERBOARD_TITLE}",
			"@{LEADERBOARD_JUMBO_TITLE}",
			"leaderboard.php",
			true
		);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {
		$leaderboard = new LeaderboardTable($this->dictionary, $this->user);
		return [$leaderboard];
	}
}