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

namespace bundesliga_tippspiel_kudubot_communication;
use SQLite3;

/**
 * Class KudubotDb
 * Class that automatically opens a connection to the kudubot database
 * @package bundesliga_tippspiel_kudubot_communication
 */
class KudubotDb extends SQLite3 {

	/**
	 * KudubotDb constructor.
	 * Opens the database connection
	 * @param string $connection_name: The kudubot connection to use
	 */
	function __construct(string $connection_name) {
		parent::__construct(
			__DIR__ . "/../../../kudubot/data/" .
			$connection_name . ".db"
		);
	}
}


/**
 * Class KudubotCommunication
 * Class that contains various kudubot-related functions
 * @package bundesliga_tippspiel_kudubot_communication
 */
class KudubotCommunication {

	/**
	 * Checks if the user is registered or not
	 * @param int $user_id : The user's ID
	 * @param string $connection : The connection to check the status for
	 * @return bool: true if the user is registered, false otherwise
	 */
	static function getRegisteredStatus(int $user_id, string $connection) {
		$db = new KudubotDb($connection);
		/** @noinspection SqlDialectInspection */
		/** @noinspection SqlNoDataSourceInspection */
		$stmt = $db->prepare(
			"SELECT verified FROM bundesliga_tippspiel_reminder " .
			"WHERE user_id=?"
		);
		$stmt->bindParam(1, $user_id, SQLITE3_INTEGER);
		$result = $stmt->execute();
		$row = $result->fetchArray();
		$next = $result->fetchArray();
		print_r($row["verified"]);

		$db->close();

		return (
			$row !== null && $next === null
			&&
			(int)$row["verified"] === 1
		);
	}

	/**
	 * Registers a connection for reminding a user
	 * of a match they have not yet bet on
	 * @param int $user_id : The user's ID
	 * @param string $username : The user's username
	 * @param string $connection : The kudubot connection to register
	 * @param int $warningTime : The amount of time before the match that the user
	 *                          wants to be reminded
	 * @return string: The message the user needs to send to kudubot to complete
	 *                 the registration process
	 */
	static function register(int $user_id, string $username,
					  string $connection, int $warningTime): string {

		$key = bin2hex(random_bytes(12));
		$hash = password_hash($key, PASSWORD_BCRYPT);

		$db = new KudubotDb($connection);
		/** @noinspection SqlNoDataSourceInspection */
		/** @noinspection SqlDialectInspection */
		$stmt = $db->prepare(
			"INSERT OR REPLACE INTO bundesliga_tippspiel_reminder " .
			"(user_id, username, address, key_hash," .
			"verified, warning_time, last_match) " .
			"VALUES (?, ?, NULL, ?, 0, ?, NULL)"
		);
		$stmt->bindParam(1, $user_id, SQLITE3_INTEGER);
		$stmt->bindParam(2, $username, SQLITE3_TEXT);
		$stmt->bindParam(3, $hash, SQLITE3_TEXT);
		$stmt->bindParam(4, $warningTime, SQLITE3_INTEGER);
		$stmt->execute();
		$db->close();

		return (string)$user_id . ":" . $key;
	}

	/**
	 * Unsubscribes a user from reminders for a particular kudubot connection
	 * @param int $user_id : The user's ID
	 * @param string $connection : The connection to de-register
	 */
	static function deRegister(int $user_id, string $connection) {
		$db = new KudubotDb($connection);
		/** @noinspection SqlNoDataSourceInspection */
		/** @noinspection SqlDialectInspection */
		$stmt = $db->prepare(
			"DELETE FROM bundesliga_tippspiel_reminder WHERE user_id=?"
		);
		$stmt->bindParam("i", $user_id);
		$stmt->execute();
		$db->close();

	}

	/**
	 * Checks if a connection is a valid option
	 * @param string $connection : The connection to check
	 * @return bool: true if the connection is valid, false otherwise
	 */
	static function isValidConnection(string $connection): bool {
		return in_array($connection, ["whatsapp", "telegram"]);
	}
}