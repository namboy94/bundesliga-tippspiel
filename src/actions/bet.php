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
require __DIR__ . '/../../vendor/autoload.php';
use bundesliga_tippspiel\Functions;
use cheetah\BetManager;
use cheetah\Match;
use cheetah\SeasonManager;
use welwitschi\Authenticator;
use ErrorException;

Functions::initializeSession();

/**
 * Places a bet
 */
function bet() {

	$auth = new Authenticator(Functions::getMysqli());
	$db = Functions::getMysqli();
	$seasonManager = new SeasonManager($db);

	if (!isset($_POST["matchday_referrer"]) ||
		(int)$_POST["matchday_referrer"] < 1 ||
		(int)$_POST["matchday_referrer"] > $seasonManager->getMaxMatchday()) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{BET_FAIL_INVALID_MATCHDAY_TITLE}",
			"body" => "@{BET_FAIL_INVALID_MATCHDAY_BODY}"
		];
		header("Location: ../bets.php");

	} elseif (isset($_SESSION["user_id"])) {
		$user = $auth->getUserFromId($_SESSION["user_id"]);
		if ($user !== null) {

			$betManager = new BetManager($db);

			$matchDay = (int)$_POST["matchday_referrer"];
			$matches = Match::getAllForMatchday($db, $matchDay);

			$errors = false;

			foreach ($matches as $match) {
				$homeScore = $_POST[$match->homeTeam->id];
				$awayScore = $_POST[$match->awayTeam->id];

				if ($homeScore === "" || $awayScore === "") {
					continue;  // Skip unentered fields
				}

				$homeScore = (int)$homeScore;
				$awayScore = (int)$awayScore;

				if ($homeScore < 1000 && $homeScore >= 0 &&
					$awayScore < 1000 && $awayScore >= 0) {
					if (!$betManager->placeBetWithLoginSession(
						$user, $match, $homeScore, $awayScore)
					) {
						$errors = true;
					}
				} else {
					$errors = true;
				}
			}

			if ($errors) {
				$_SESSION["message"] = [
					"type" => "warning",
					"title" => "@{BET_SUCCESS_WITH_ERRORS_TITLE}",
					"body" => "@{BET_SUCCESS_WITH_ERRORS_BODY}"
				];
			} else {
				$_SESSION["message"] = [
					"type" => "success",
					"title" => "@{BET_SUCCESS_TITLE}",
					"body" => "@{BET_SUCCESS_BODY}"
				];
			}
			header("Location: ../bets.php?matchday=" . (string)$matchDay);

		} else {
			header("Location: ../index.php");
		}
	} else {
		header("Location: ../index.php");
	}
}

// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	bet();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
	throw $e;
}