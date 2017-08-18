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


use bundesliga_tippspiel_comments\CommentBar;
use bundesliga_tippspiel_comments\CommentManager;
use welwitschi\Authenticator;

/**
 * Class CommentAction
 * Action that handles new comments
 * @package bundesliga_tippspiel_actions
 */
class CommentAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: An ActionExpression containing message data
	 */
	protected function defineBehaviour() {

		if (!isset($_POST[CommentBar::$contentId])) {
			throw new DangerException("COMMENT_FAIL_NO_INPUT",
				$_SERVER['HTTP_REFERER']);
		}

		$content = $_POST[CommentBar::$contentId];
		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($_SESSION["user_id"]);
		$commentManager = new CommentManager($this->db);

		$commentManager->writeComment($user, $content);

	}
}