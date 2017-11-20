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
use bundesliga_tippspiel_api\PlaceBetsApiAction;
use cheetah\Match;


/**
 * Class PlaceBetApiActionTest
 * Tests the PlaceApi Action
 * @package bundesliga_tippspiel_tests
 */
class PlaceBetApiActionTest extends GenericApiTest {

	/**
	 * @var string: The API Key of user A
	 */
	private $apiKey;

	/**
	 * @var array: The matches of the 34th match day
	 */
	private $matches34;

	/**
	 * @var array: The matches of the 1st match day
	 */
	private $matches1;

	/**
	 * @param bool $fetchMatchData: Fetches data before the tests
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = true) {
		parent::setUpBeforeClass($fetchMatchData);
	}

	/**
	 * Stores various variables that are used often in tests
	 * Also makes sure that no bets are currently placed
	 */
	public function setUp() {
		parent::setUp();
		$this->apiKey = $this->confirmedUserA->generateNewApiKey();
		$this->matches34 = Match::getAllForMatchday(self::$db, 34);
		$this->matches1 = Match::getAllForMatchday(self::$db, 1);

		$this->assertEquals(
			count(self::$betManager->getAllBetsForUser($this->confirmedUserA)),
			0
		);
	}

	/**
	 * Tests placing a successful bets
	 */
	public function testPlacingSuccessfulBet() {

		$bets = [];
		foreach ($this->matches34 as $match) {
			array_push($bets, [
				"home_score" => 1,
				"away_score" => 2,
				"match_id" => $match->id
			]);
		}

		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "A",
			"api_key" => $this->apiKey,
			"bets" => $bets
		]);

		$this->assertEquals($result["status"], "success");
		$newBets = self::$betManager->getAllBetsForUserOnMatchday(
			$this->confirmedUserA, 34);

		$this->assertEquals(count($newBets), 9);
		foreach ($newBets as $bet) {
			$this->assertEquals($bet->homeScore, 1);
			$this->assertEquals($bet->awayScore, 2);
		}
	}

	/**
	 * Tests placing no bets
	 */
	public function testPlacingEmptyBet() {
		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "A",
			"api_key" => $this->apiKey,
			"bets" => []
		]);
		$this->assertEquals($result["status"], "success");
		$this->assertEquals(
			count(self::$betManager->getAllBetsForUser($this->confirmedUserA)),
			0
		);
	}

	/**
	 * Tests placing invalid bets
	 */
	public function testPlacingInvalidBets() {

		$options = [
			["home_score" => 1, "away_score" => 1],
			["home_score" => 1, "match_id" => 1],
			["away_score" => 1, "match_id" => 1],
			["home_score" => "AA", "away_score" => 1, "match_id" => 1],
			["home_score" => 1, "away_score" => "0", "match_id" => 1],
			["home_score" => 1, "away_score" => 1, "match_id" => ""],
			["home_score" => -1, "away_score" => 1, "match_id" => 1],
			["home_score" => 1, "away_score" => -1, "match_id" => 1],
			["home_score" => 1000, "away_score" => 1, "match_id" => 1],
			["home_score" => 1, "away_score" => 1000, "match_id" => 1]
		];

		foreach ($options as $option) {
			$result = $this->executeApiAction(PlaceBetsApiAction::class, [
				"username" => "A",
				"api_key" => $this->apiKey,
				"bets" => [$option]
			]);
			$this->assertEquals($result["status"], "error");
			$this->assertEquals($result["cause"], "invalid_bet");
		}
	}

	/**
	 * Tests placing an invalid bet among other valid bets
	 */
	public function testPlacingInvalidBetAmongValidBets() {

		$bets = [];
		foreach ($this->matches34 as $match) {
			array_push($bets, [
				"home_score" => 1,
				"away_score" => 2,
				"match_id" => $match->id
			]);
		}
		$bets[17]["home_score"] = -1;

		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "A",
			"api_key" => $this->apiKey,
			"bets" => $bets
		]);

		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "invalid_bet");
	}

	/**
	 * Tests placing bets on matches that have already started
	 */
	public function testBettingOnStartedMatches() {
		$bets = [];
		foreach ($this->matches1 as $match) {
			array_push($bets, [
				"home_score" => 1,
				"away_score" => 2,
				"match_id" => $match->id
			]);
		}

		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "A",
			"api_key" => $this->apiKey,
			"bets" => $bets
		]);

		$this->assertEquals($result["status"], "success_with_errors");
		$newBets = self::$betManager->getAllBetsForUserOnMatchday(
			$this->confirmedUserA, 1);
		$this->assertEquals(count($newBets), 0);
	}

	/**
	 * Tests placing a bet as an unauthorized user
	 */
	public function testBettingAsUnauthorizedUser() {
		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "A",
			"api_key" => "A",
			"bets" => []
		]);
		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "unauthorized");

		$result = $this->executeApiAction(PlaceBetsApiAction::class, [
			"username" => "B",
			"api_key" => $this->apiKey,
			"bets" => []
		]);
		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "unauthorized");
	}

}