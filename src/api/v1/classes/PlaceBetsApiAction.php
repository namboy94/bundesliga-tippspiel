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

namespace bundesliga_tippspiel_api;
use cheetah\BetManager;
use cheetah\Match;

/**
 * Class PlaceBetsForMatchdayApiAction
 * This API Action allows a user to place bets
 * @package bundesliga_tippspiel_api
 */
class PlaceBetsApiAction extends ApiAction {

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: If the API Action could not be completed
	 * @SuppressWarnings docBlocks
	 */
	protected function defineBehaviour(): array {

		$user = $this->authenticator->getUserFromUsername(
			$this->inputData["username"]);
		$apiKey = $this->inputData["api_key"];
		$betManager = new BetManager($this->db);

		// Make sure all bets are OK
        foreach ($this->inputData["bets"] as $bet) {
            if (!$this->_checkBetValidity($bet)) {
                throw new ApiException("invalid_bet");
            }
        }

		$errors = false;
		foreach ($this->inputData["bets"] as $bet) {
            $homeScore = (int)$bet["home_score"];
            $awayScore = (int)$bet["away_score"];
            $matchId = (int)$bet["match_id"];
            $match = Match::fromId($this->db, $matchId);

            /** @noinspection PhpUndefinedMethodInspection */
            if ($match->hasStarted()) {
                $errors = true;  // Skip this bet
            } else {
                /** @noinspection PhpParamsInspection */
                $errors = $errors || !$betManager->placeBetWithApiKey(
                        $user, $apiKey, $match, $homeScore, $awayScore);
            }
		}

		$resultName = $errors ? "success_with_errors" : "success";
		return ["status" => $resultName];
	}

	/**
	 * Checks if a bet is valid
	 * @param array $bet: The bet to check
	 * @return bool: true if the bet is valid, false otherwise
	 */
	private function _checkBetValidity(array $bet) : bool {

		if (!isset($bet["home_score"]) ||
			!isset($bet["away_score"]) ||
			!isset($bet["match_id"])) {
			return false;
		}

		if (!is_int($bet["home_score"]) ||
			!is_int($bet["away_score"]) ||
			!is_int($bet["match_id"])) {
			return false;
		}

		$homeScore = $bet["home_score"];
		$awayScore = $bet["away_score"];

		if ($homeScore >= 100 || $homeScore < 0 ||
				$awayScore >= 100 || $awayScore < 0) {
			return false;
		}
		return true;
	}

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public function defineRequiredParameters(): array {
		return ["bets"];
	}
}