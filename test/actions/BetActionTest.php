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

namespace bundesliga_tippspiel_tests;
use bundesliga_tippspiel_actions\BetAction;
use cheetah\Bet;
use cheetah\Match;

/**
 * Class BetActionTest
 * Test the Bet Action class
 */
class BetActionTest extends TestClass {

	/**
	 * Fetch data beforehand
	 * @param bool $fetchMatchData: true
	 * @SuppressWarnings checkUnusedFunctionParameters
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = false) {
		parent::setUpBeforeClass(true);
	}

	/**
	 * Tests placing some valid bets using the BetAction class
	 */
	public function testPlacingValidBets() {

		$matches = Match::getAllForMatchday(self::$db, 34);
		foreach ($matches as $match) {
			$_POST[$match->homeTeam->id] = 1;
			$_POST[$match->awayTeam->id] = 3;
		}
		$_POST["matchday_referrer"] = 34;

		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "success");

		foreach ($matches as $match) {
			$bet = Bet::fromMatchAndUserId(
				self::$db, $match->id, $this->confirmedUserA->id);

			/** @noinspection PhpUndefinedFieldInspection */
			$this->assertEquals(1, $bet->homeScore);
			/** @noinspection PhpUndefinedFieldInspection */
			$this->assertEquals(3, $bet->awayScore);
		}
	}

	/**
	 * Tests betting on a single match instead of all 9 matches on a matchday
	 */
	public function testBettingOnSingleMatch() {
		$matches = Match::getAllForMatchday(self::$db, 34);
		$match = array_pop($matches);
		$_POST["matchday_referrer"] = 34;
		$_POST[$match->homeTeam->id] = 0;
		$_POST[$match->awayTeam->id] = 2;

		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "success");
		$bet = Bet::fromMatchAndUserId(
			self::$db, $match->id, $this->confirmedUserA->id);

		/** @noinspection PhpUndefinedFieldInspection */
		$this->assertEquals(0, $bet->homeScore);
		/** @noinspection PhpUndefinedFieldInspection */
		$this->assertEquals(2, $bet->awayScore);
	}

	/**
	 * Tests using an invalid matchday
	 */
	public function testInvalidMatchday() {
		$_POST["matchday_referrer"] = 35;
		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "danger");
		$this->assertStringStartsWith("@{BET_FAIL_INVALID_MATCHDAY",
			$_SESSION["message"]["title"]);

		$_POST["matchday_referrer"] = 0;
		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "danger");
		$this->assertStringStartsWith("@{BET_FAIL_INVALID_MATCHDAY",
			$_SESSION["message"]["title"]);
	}

	/**
	 * Tests using various invalid bet values
	 */
	public function testInvalidBetValues() {

		$matches = Match::getAllForMatchday(self::$db, 34);
		$match = array_pop($matches);

		// No bets at all
		$_POST["matchday_referrer"] = 34;
		(new BetAction())->execute();

		$this->assertEquals($_SESSION["message"]["type"], "success");

		$_POST[$match->homeTeam->id] = -1;
		$_POST[$match->awayTeam->id] = 1;
		(new BetAction())->execute();

		$this->assertEquals($_SESSION["message"]["type"], "success");
		$this->assertNull(Bet::fromMatchAndUserId(
			self::$db, $match->id, $this->confirmedUserA->id));

		$_POST[$match->homeTeam->id] = 1;
		$_POST[$match->awayTeam->id] = "";
		(new BetAction())->execute();

		$this->assertEquals($_SESSION["message"]["type"], "success");
		$this->assertNull(Bet::fromMatchAndUserId(
			self::$db, $match->id, $this->confirmedUserA->id));

	}

	/**
	 * Tests betting on matches that have already started
	 */
	public function testPlacingBetsOnStartedMatches() {

		$matches = Match::getAllForMatchday(self::$db, 1);
		foreach ($matches as $match) {
			$_POST[$match->homeTeam->id] = 2;
			$_POST[$match->awayTeam->id] = 1;
		}
		$_POST["matchday_referrer"] = 33;

		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "warning");
		$this->assertStringStartsWith("@{BET_SUCCESS_WITH_ERRORS",
			$_SESSION["message"]["title"]);

		foreach ($matches as $match) {
			$this->assertNull(Bet::fromMatchAndUserId(
				self::$db, $match->id, $this->confirmedUserA->id));
		}
	}

	/**
	 * Tests placing bets as an unauthorized user
	 */
	public function testBettingWithUnauthorizedUser() {

		$this->confirmedUserA->logout();
		$_POST["matchday_referrer"] = 34;

		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "danger");
		$this->assertStringStartsWith("@{BET_FAIL_INVALID_USER",
			$_SESSION["message"]["title"]);

		$this->confirmedUserA->login("A");
		$_SESSION["login_token"] = "A";

		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "danger");
		$this->assertStringStartsWith("@{BET_FAIL_UNAUTHORIZED",
			$_SESSION["message"]["title"]);

		$_SESSION["user_id"] = -1;
		(new BetAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "danger");
		$this->assertStringStartsWith("@{BET_FAIL_INVALID_USER",
			$_SESSION["message"]["title"]);
	}
}