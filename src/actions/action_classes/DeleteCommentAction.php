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
use bundesliga_tippspiel_comments\CommentManager;
use welwitschi\Authenticator;

/**
 * Class DeleteCommentAction
 * Enables the user to delete a comment
 * @package bundesliga_tippspiel_actions
 */
class DeleteCommentAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: The message information
	 */
	protected function defineBehaviour() {
		$commentId = $_GET["comment"];
		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($_SESSION["user_id"]);

		$commentManager = new CommentManager($this->db);
		$result = $commentManager->deleteCommentById($user, $commentId);

		if (!$result) {
			throw new DangerException("COMMENT_DELETE_FAIL",
				$_SERVER["HTTP_REFERER"]);
		}
	}
}