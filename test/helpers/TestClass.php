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
use bundesliga_tippspiel_comments\CommentManager;
use cheetah\BetManager;
use cheetah\SchemaCreator;
use mysqli;
use PHPUnit\Framework\TestCase;
use welwitschi\Authenticator;
use welwitschi\User;

/**
 * Class BetActionTest
 * Sets up common use cases
 */
class TestClass extends TestCase {

	/**
	 * @var mysqli: The database connection to use
	 */
	static protected $db;

	/**
	 * @var User: A confirmed user
	 */
	static protected $confirmedUserA;

	/**
	 * @var User: A unconfirmed user
	 */
	static protected $unConfirmedUserB;

	/**
	 * @var Authenticator: An authenticator
	 */
	static protected $authenticator;

	/**
	 * @var BetManager: A BetManager
	 */
	static protected $betManager;

	/**
	 * @var CommentManager: A comment manager
	 */
	static protected $commentManager;

	/**
	 * Creates Databases and objects
	 * @param bool $fetchMatchData: Set to true to fetch match data
	 * @SuppressWarnings checkProhibitedFunctions
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = false) {
		parent::setUpBeforeClass();

		self::$db = self::getDb();

		self::$authenticator = new Authenticator(self::$db);
		self::$commentManager = new CommentManager(self::$db);
		self::$betManager = new BetManager(self::$db);
		new SchemaCreator(self::$db);

		self::$authenticator->createUser("A", "A", "A");
		self::$authenticator->createUser("B", "B", "B");
		self::$confirmedUserA = self::$authenticator->getUserFromUsername("A");
		self::$unConfirmedUserB =
			self::$authenticator->getUserFromUsername("B");
		self::$confirmedUserA->confirm(
			self::$confirmedUserA->confirmationToken);

		if ($fetchMatchData) {
			exec("python vendor/namboy94/cheetah-bets/scripts/leaguegetter.py" .
				" phpunit " . getenv("TEST_DB_PASS") .
				" bundesliga_tippspiel_bets_test -s 2016");

			self::$db->query(
				"UPDATE matches " .
				"SET finished=0, kickoff='3000-01-01T00:00:00Z' " .
				"WHERE matchday=34;"
			);
		}
		self::$db->commit();
	}

	/**
	 * Deletes database tables
	 */
	public static function tearDownAfterClass() {
		parent::tearDownAfterClass();
		self::$db->query(
			"DROP TABLE comments; DROP TABLE bets; DROP TABLE goals;" .
			"DROP TABLE players; DROP TABLE matches; DROP TABLE teams;" .
			"DROP TABLE sessions; DROP TABLE accounts;");
		self::$db->commit();
		self::$db->close();
	}

	/**
	 * Deletes content in database
	 */
	public function setUp() {
		parent::setUp();
		self::$db->query("DELETE FROM accounts;");
		self::$db->commit();
	}

	/**
	 * @return mysqli: The Database connection to be used in testing
	 */
	protected static function getDb() : mysqli {
		return new mysqli(
			"localhost",
			"phpunit",
			getenv("TEST_DB_PASS"), // Uses environment variable
			"bundesliga_tippspiel_test"
		);
	}
}