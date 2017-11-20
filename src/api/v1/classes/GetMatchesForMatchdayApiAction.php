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
use cheetah\SeasonManager;

/**
 * Class GetUserBetsForMatchdayApiAction
 * This API Action allows the retrieval of bets for a given matchday
 * for a single user. Includes information about the match and teams.
 * @package bundesliga_tippspiel_api
 */
class GetMatchesForMatchdayApiAction extends ApiAction {

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: If the API Action could not be completed
	 * @SuppressWarnings docBlocks
	 */
	protected function defineBehaviour(): array {
		$seasonManager = new SeasonManager($this->db);

		if (!isset($this->inputData["matchday"])) {
			$matchday = $seasonManager->getCurrentMatchday();
		} else {
			$matchday = (int)$this->inputData["matchday"];
		}

		if ($matchday < 1 || $matchday > $seasonManager->getMaxMatchday()) {
			throw new ApiException("invalid_matchday");
		}

		$matches = Match::getAllForMatchday($this->db, $matchday);

		$result = [];
		foreach ($matches as $match) {
			/** @noinspection PhpUndefinedMethodInspection */
			array_push($result, $match->toArray());
		}
		return ["data" => $result];
	}

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public function defineRequiredParameters(): array {
		return [];
	}
}