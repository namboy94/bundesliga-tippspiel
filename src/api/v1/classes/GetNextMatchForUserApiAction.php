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

namespace bundesliga_tippspiel_api;
use cheetah\Match;

/**
 * Class GetNextMatchForUserApiAction
 * Class that implements an API endpoint that enables getting the next match
 * on which a user has not yet bet on
 * @package bundesliga_tippspiel_api
 */
class GetNextMatchForUserApiAction extends ApiAction {

	/**
	 * GetRankingsApiAction constructor.
	 * This Constructor overrides the default API Action behaviour that
	 * requires authentication.
	 * @param bool $authenticationRequired: Set to false
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: If the API Action could not be completed
	 */
	protected function defineBehaviour(): array {

		if (!isset($_GET["user"])) {
			throw new ApiException("No user ID provided");
		}

		$stmt = $this->db->prepare(
			"SELECT MAX(matches.kickoff) AS kickoff " .
			"FROM matches JOIN bets ON matches.id=bets.match_id " .
			"WHERE bets.user_id=?"
		);
		$stmt->bind_param("i", $_GET["user"]);
		$stmt->execute();
		$result = $stmt->get_result()->fetch_array(MYSQLI_ASSOC);
		$last_bet = $result["kickoff"];

		$stmt = $this->db->prepare(
			"SELECT MIN(id) AS id, MIN(kickoff) AS kickoff " .
			"FROM matches WHERE kickoff > ?"
		);
		$stmt->bind_param("s", $last_bet);
		$stmt->execute();
		$match_id = $stmt->get_result()->fetch_array(MYSQLI_ASSOC)["id"];
		$match = Match::fromId($this->db, $match_id);

		return ["data" => $match->toArray()];
	}

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public function defineRequiredParameters(): array {
		return [];
	}
}