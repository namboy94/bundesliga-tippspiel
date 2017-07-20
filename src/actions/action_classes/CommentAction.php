<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/20/17
 * Time: 8:49 AM
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