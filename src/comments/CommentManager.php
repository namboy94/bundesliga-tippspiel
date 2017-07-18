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

namespace bundesliga_tippspiel_comments;
use mysqli;
use welwitschi\User;

/**
 * Class SchemaCreator
 * Class that offers methods to access and modify comments
 * @package bundesliga_tippspiel_comments
 */
class CommentManager {

	/**
	 * CommentManager constructor.
	 * @param mysqli $db: The database connection to use
	 */
	function __construct(mysqli $db) {
		$this->db = $db;
		self::createCommentsTable($db);
	}

	/**
	 * Creates the comments database table
	 * @param mysqli $db: The database connection to use
	 */
	public static function createCommentsTable(mysqli $db) {
		$db->query(
			"CREATE TABLE IF NOT EXISTS comments (" .
			"    id INTEGER NOT NULL AUTO_INCREMENT," .
			"    user_id INTEGER NOT NULL," .
			"    content VARCHAR(255) NOT NULL," .
			"    timestamp INTEGER NOT NULL," .
			"    PRIMARY KEY(id)," .
			"    FOREIGN KEY(user_id) references accounts(id)" .
			"        ON DELETE CASCADE" .
			"        ON UPDATE CASCADE" .
			");"
		);
		$db->commit();
	}

	/**
	 * Retrieves all comments up to a limit
	 * @param $limit: The limit up to which to retrieve comments
	 * @return array: The $limit newest comments
	 */
	public function getComments(int $limit = 50) : array {
		$stmt = $this->db->prepare(
			"SELECT * FROM comments ORDER BY timestamp DESC LIMIT ?"
		);
		$stmt->bind_param("i", $limit);
		$stmt->execute();
		$results = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);

		$comments = [];
		foreach ($results as $result) {
			array_push($comments, Comment::fromRow($this->db, $result));
		}
		return $comments;
	}

	/**
	 * Writes a comment
	 * Only a logged in user can write comments
	 * @param User $user: The user that writes the comment
	 * @param string $content: The content to write
	 * @return bool: true if the comment was written successfully, else false
	 */
	public function writeComment(User $user, string $content) : bool {
		if ($user->isLoggedIn()) {

			$content = htmlspecialchars($content); // XSS Protection :)
			$timestamp = time();

			$stmt = $this->db->prepare(
				"INSERT INTO comments (user_id, content, timestamp) " .
				"VALUES (?, ?, ?);"
			);
			$stmt->bind_param("isi", $user->id, $content, $timestamp);
			$result = $stmt->execute();
			return $result !== false;

		} else {
			return false;
		}
	}

	/**
	 * Deletes a comment from the database
	 * @param User $user: The user that tries to delete this comment
	 * @param Comment $comment: The comment to be deleted
	 * @return bool: true if the delete operation was successful
	 */
	public function deleteComment(User $user, Comment $comment) : bool {
		return $this->deleteCommentById($user, $comment->id);
	}

	/**
	 * Deletes a comment from the database using the comment ID.
	 * Only a logged in user can delete comments
	 * @param User $user: The user that initiated the deletion
	 * @param int $commentId: The comment ID of the comment to delete
	 * @return bool: true if the deletion was successful, false otherwise
	 */
	public function deleteCommentById(User $user, int $commentId) : bool {
		if ($user->isLoggedIn()) {

			$stmt = $this->db->prepare(
				"DELETE FROM comments WHERE id=? AND user_id=?;"
			);
			$stmt->bind_param("si", $commentId, $user->id);
			$result = $stmt->execute();
			$this->db->commit();
			return $result !== false;

		} else {
			return false;
		}
	}

}