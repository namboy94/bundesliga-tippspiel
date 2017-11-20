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

namespace bundesliga_tippspiel_tests;


use bundesliga_tippspiel_api\GetUserBetsForMatchdayApiAction;
use cheetah\Match;

/**
 * Class GetUserBetsForMatchdayApiActionTest
 * @package bundesliga_tippspiel_tests
 */
class GetUserBetsForMatchdayApiActionTest extends GenericApiTest {

	/**
	 * @param bool $fetchMatchData: Fetches data before the tests
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = true) {
		parent::setUpBeforeClass($fetchMatchData);
	}

	/**
	 * Places bets on matchday 34
	 * @SuppressWarnings checkUnusedVariables
	 */
	public function setUp() {
		parent::setUp();
		$matches = Match::getAllForMatchday(self::$db, 34);
		foreach ($matches as $match) {
			self::$betManager->placeBetWithoutAuthentication(
				$this->confirmedUserA, $match, 1, 1);
		}
	}

	/**
	 * Tests retrieving the bets of a user for matchday 34
	 */
	public function testGettingBets() {
		$result = $this->executeApiAction(
			GetUserBetsForMatchdayApiAction::class,
			[
				"username" => $this->confirmedUserA->username,
				"api_key" => $this->confirmedUserA->generateNewApiKey(),
				"matchday" => 34
			]
		);

		$this->assertEquals($result["status"], "success");
		$this->assertEquals(count($result["data"]), 9);
		$this->assertEquals($result["data"][0]["home_score"], 1);
		$this->assertEquals($result["data"][0]["away_score"], 1);
	}

	/**
	 * Tests trying to use the API endpoint when no
	 * matchday parameter was specified, which should then default to the
	 * current matchday
	 */
	public function testWithMissingMatchdayParameter() {

		$result = $this->executeApiAction(
			GetUserBetsForMatchdayApiAction::class,
			[
				"username" => $this->confirmedUserA->username,
				"api_key" => $this->confirmedUserA->generateNewApiKey()
			]
		);

		$this->assertEquals($result["status"], "success");
		$this->assertEquals(count($result["data"]), 9);
		$this->assertEquals($result["data"][0]["home_score"], 1);
		$this->assertEquals($result["data"][0]["away_score"], 1);

	}

	/**
	 * Tests retrieving bets for an invalid matchday
	 */
	public function testGettingBetsForInvalidMatchday() {

		foreach ([ -1, 35, 0] as $matchday) {
			$result = $this->executeApiAction(
				GetUserBetsForMatchdayApiAction::class,
				[
					"username" => $this->confirmedUserA->username,
					"api_key" => $this->confirmedUserA->generateNewApiKey(),
					"matchday" => $matchday
				]
			);

			$this->assertEquals($result["status"], "error");
			$this->assertEquals($result["cause"], "invalid_matchday");
		}
	}

	/**
	 * Tests retrieving the bets for a user on matchday where no bets have
	 * been placed by said user
	 */
	public function testGettingBetsOnMatchdayWithoutBets() {

		$result = $this->executeApiAction(
			GetUserBetsForMatchdayApiAction::class,
			[
				"username" => $this->confirmedUserA->username,
				"api_key" => $this->confirmedUserA->generateNewApiKey(),
				"matchday" => 17
			]
		);

		$this->assertEquals($result["status"], "success");
		$this->assertEquals(count($result["data"]), 0);
	}

}