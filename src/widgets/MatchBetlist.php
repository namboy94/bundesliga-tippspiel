<?php
/**
 * Copyright Hermann Krumrey <hermann@krumreyh.com> 2017
 *
 * This file is part of bundesliga_tippspiel.
 *
 * bundesliga_tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga_tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga_tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use cheetah\Bet;
use cheetah\Match;
use welwitschi\Authenticator;
use welwitschi\User;


/**
 * Class MatchBetlist
 * Displays the bets of each user on a particular match.
 * If the match has not started yet, only the active user's bet is
 * displayed.
 * @package bundesliga_tippspiel
 */
class MatchBetlist extends HtmlTemplate {

	/**
	 * MatchBetlist constructor.
	 * @param Dictionary|null $dictionary: The dictionary to use
	 * @param Match $match: The match to display the user bets for
	 * @param User $activeUser: The user that called this page
	 */
	public function __construct(
		? Dictionary $dictionary, Match $match, User $activeUser
	) {

		$db = Functions::getMysqli();
		$auth = new Authenticator($db);
		$users = $auth->getAllUsers();

		$entries = [];
		foreach ($users as $user) {

			if ($user->id !== $activeUser->id && !$match->hasStarted()) {
				continue;  // Skip other users if match has not started yet
			}

			$bet = Bet::fromMatchAndUserId($db, $match->id, $user->id);
			/** @noinspection PhpUndefinedMethodInspection */
			$points = $bet === null ? "-" : $bet->evaluate();
			switch ($points) {
				case 0: $badge = "danger"; break;
				case 1: $badge = "warning"; break;
				case 2: $badge = "default"; break;
				case 3: $badge = "info"; break;
				case 4: $badge = "primary"; break;
				case 5: $badge = "success"; break;
				default: $badge = "default";
			}

			$betlistEntry = new HtmlTemplate(
				__DIR__ . "/templates/match_betlist_entry.html", $dictionary
			);

			/** @noinspection PhpUndefinedFieldInspection */
			$betlistEntry->bindParams([
				"USERNAME" => $user->username,
				"USER_HOME_SCORE" => ($bet === null) ? "-" : $bet->homeScore,
				"USER_AWAY_SCORE" => ($bet === null) ? "-" : $bet->awayScore,
				"LABEL_COLOR" => $badge,
				"USER_POINTS" => $points
			]);

			array_push($entries, $betlistEntry);

		}

		$db->close();

		parent::__construct(
			__DIR__ . "/templates/match_betlist.html", $dictionary
		);

		$this->bindParams([
			"HOME_NAME_TITLE" => $match->homeTeam->abbreviation,
			"AWAY_NAME_TITLE" => $match->awayTeam->abbreviation
		]);
		$this->addCollectionFromArray("ENTRIES", $entries);
	}

}