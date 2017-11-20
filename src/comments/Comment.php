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

namespace bundesliga_tippspiel_comments;
use mysqli;
use welwitschi\Authenticator;
use welwitschi\User;


/**
 * Class Comment
 * Models a Comment object that refers to a row in the database
 * @package bundesliga_tippspiel_comments
 */
class Comment {

	/**
	 * Comment constructor.
	 * @param int $id
	 * @param User $user
	 * @param string $content
	 * @param int $timestamp
	 */
	public function __construct(
		int $id, User $user, string $content, int $timestamp) {

		$this->id = $id;
		$this->user = $user;
		$this->content = $content;
		$this->timestamp = $timestamp;
	}

	/**
	 * Creates a new Comment object from a row from the database
	 * @param mysqli $db: The database connection to use
	 * @param array $row: The row to convert into this object
	 * @return Comment: The generated Comment object
	 */
	public static function fromRow(mysqli $db, array $row) {
		$auth = new Authenticator($db);
		$user = $auth->getUserFromId((int)$row["user_id"]);
		return new Comment(
			(int)$row["id"],
			$user,
			(string)$row["content"],
			(int)$row["timestamp"]
		);
	}
}