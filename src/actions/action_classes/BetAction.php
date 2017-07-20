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

namespace bundesliga_tippspiel_actions;
use cheetah\BetManager;
use cheetah\Match;
use cheetah\SeasonManager;
use welwitschi\Authenticator;
use welwitschi\User;

/**
 * Class BetAction
 * Handles placing a bet
 * @package bundesliga_tippspiel_actions
 */
class BetAction extends Action {

	/**
	 * Validates the input and ultimately places a bet if everything is fine
	 *
	 * @return void
	 * @throws ActionException
	 */
	protected function defineBehaviour() {

		$matchDay = $this->_getMatchday();
		$user = $this->_getUser();

		$matches = Match::getAllForMatchday($this->db, $matchDay);
		$betManager = new BetManager($this->db);

		$errors = false;

		foreach ($matches as $match) {

			$scores = $this->_getScores($match);

			if ($scores === null) {
				continue;  // Skip unentered fields
			}

			$errors = $errors || !$betManager->placeBetWithLoginSession(
				$user, $match, $scores["home"], $scores["away"]);
		}

		$redirect = "../bets.php?matchday=" . (string)$matchDay;
		if ($errors) {
			throw new WarningException("BET_SUCCESS_WITH_ERRORS", $redirect);
		} else {
			throw new SuccessException("BET_SUCCESS", $redirect);
		}

	}

	/**
	 * Checks the matchday_referrer POST variable, makes ure it is valid
	 * and then returns it
	 * @return int: The matchday_referrer variable as an int
	 * @throws DangerException: If the POST variable is invalid
	 */
	private function _getMatchday() : int {

		$seasonManager = new SeasonManager($this->db);

		$maxMatchDay = $seasonManager->getMaxMatchday();
		if (!isset($_POST["matchday_referrer"]) ||
			(int)$_POST["matchday_referrer"] < 1 ||
			(int)$_POST["matchday_referrer"] > $maxMatchDay) {

			throw new DangerException(
				"BET_FAIL_INVALID_MATCHDAY",
				"Location: ../bets.php"
			);
		}

		return (int)$_POST["matchday_referrer"];
	}

	/**
	 * Retrieves the User based on the POST variable
	 * Also checks if the user is logged in or not. If not, a
	 * DangerException is thrown
	 * @return User: The retrieved User object
	 * @throws DangerException: If either the POST variable is not set or the
	 *                          user does not exist
	 * @throws DangerException: If the user is not logged in
	 */
	private function _getUser() : User {

		$error = new DangerException("BET_FAIL_INVALID_USER", "../index.php");

		if (!isset($_SESSION["user_id"])) {
			throw $error;
		}

		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($_SESSION["user_id"]);

		if ($user === null) {
			throw $error;

		} elseif (!$user->isLoggedIn()) {
			throw new DangerException("BET_FAIL_UNAUTHORIZED", "../index.php");

		} else {
			return $user;
		}
	}

	/**
	 * Retrieves the bet scores from the POST variable for a specific match
	 * If those are either missing or not set, null is returned.
	 * Also makes sure that the value are between 0 and 100
	 * @param Match $match: The match to retrieve the bet scores for
	 * @return array|null: an associative array with the 'home' and 'away'
	 *                     scores. If the variables aren't set, null will be
	 *                     returned instead
	 */
	private function _getScores(Match $match) : ? array {

		if (!isset($_POST[$match->homeTeam->id]) ||
			!isset($_POST[$match->awayTeam->id])) {
			return null;
		}

		$homeScore = $_POST[$match->homeTeam->id];
		$awayScore = $_POST[$match->awayTeam->id];

		if ($homeScore === "" || $awayScore === "") {
			return null;
		}

		$homeScore = (int)$homeScore;
		$awayScore = (int)$awayScore;

		if ($homeScore >= 100 || $homeScore < 0 ||
			$awayScore >= 100 || $awayScore < 0) {
			return null;
		}

		return ["home" => $homeScore, "away" => $awayScore];

	}
}
