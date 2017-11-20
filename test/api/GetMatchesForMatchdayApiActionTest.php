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
use bundesliga_tippspiel_api\GetMatchesForMatchdayApiAction;

/**
 * Class GetMatchesForMatchdayApiActionTest
 * @package bundesliga_tippspiel_tests
 */
class GetMatchesForMatchdayApiActionTest extends GenericApiTest {

	/**
	 * @param bool $fetchMatchData: Fetches data before the tests
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = true) {
		parent::setUpBeforeClass($fetchMatchData);
	}

	/**
	 * Tests successfully getting matches for a matchday
	 */
	public function testGettingMatchesForSpecificMatchday() {

		$result = $this->executeApiAction(
			GetMatchesForMatchdayApiAction::class,
			[
				"username" => $this->confirmedUserA->username,
				"api_key" => $this->confirmedUserA->generateNewApiKey(),
				"matchday" => 1
			]
		);

		$this->assertEquals($result["status"], "success");
		$this->assertEquals(count($result["data"]), 9);
		$this->assertTrue($result["data"][0]["finished"]);
		$this->assertEquals($result["data"][0]["matchday"], 1);
	}

	/**
	 * Tests successfully getting matches for the current matchday
	 */
	public function testGettingMatchesForCurrentMatchday() {

		$result = $this->executeApiAction(
			GetMatchesForMatchdayApiAction::class,
			[
				"username" => $this->confirmedUserA->username,
				"api_key" => $this->confirmedUserA->generateNewApiKey()
			]
		);

		$this->assertEquals($result["status"], "success");
		$this->assertEquals(count($result["data"]), 9);
		$this->assertFalse($result["data"][0]["finished"]);
		$this->assertEquals($result["data"][0]["matchday"], 34);
	}

	/**
	 * Tests fetching invalid match days
	 */
	public function testGettingMatchesForInvalidMatchday() {

		foreach ([ -1, 0, 35] as $matchday) {

			$result = $this->executeApiAction(
				GetMatchesForMatchdayApiAction::class,
				[
					"username" => $this->confirmedUserA->username,
					"api_key" => $this->confirmedUserA->generateNewApiKey(),
					"matchday" => $matchday,
				]
			);

			$this->assertEquals($result["status"], "error");
			$this->assertEquals($result["cause"], "invalid_matchday");

		}
	}

	/**
	 * Check if Authentication is required for this API Action
	 */
	public function testIfAuthenticationRequired() {
		$result = $this->executeApiAction(
			GetMatchesForMatchdayApiAction::class, []
		);

		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "unauthorized");
	}
}