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
use cheetah\LeaderBoard;
use welwitschi\User;


/**
 * Class LeaderboardTable
 * Displays a Table of users sorted by their points in the betting game
 * @package bundesliga_tippspiel
 */
class LeaderboardTable extends HtmlTemplate {

	/**
	 * LeaderboardTable constructor.
	 * @param Dictionary|null $dictionary: DIctionary used for translation
	 * @param User $activeUser: The active user, who will be marked in
	 *                          the ranking table
	 */
	public function __construct(
		? Dictionary $dictionary,
		User $activeUser
	) {
		parent::__construct(
			__DIR__ . "/templates/leaderboard_table.html", $dictionary
		);

		$leaderboard = new LeaderBoard(Functions::getMysqli());
		$ranking = $leaderboard->generateRanking();

		$positions = [];

		foreach ($ranking as $position => $userData) {
			$user = $userData[0];
			$points = $userData[1];

			if ($user->id === $activeUser->id) {
				$colorClass = "info";
			} elseif ($position === 1) {
				$colorClass = "success";
			} elseif ($position === count($ranking)) {
				$colorClass = "danger";
			} else {
				$colorClass = "default";
			}

			$positionElement = new LeaderboardPosition(
				$position, $user->username, $points, $colorClass
			);
			array_push($positions, $positionElement);
		}

		$this->addCollectionFromArray("POSITIONS", $positions);

	}
}