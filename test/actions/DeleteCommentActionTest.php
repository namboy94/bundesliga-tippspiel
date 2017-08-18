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
use bundesliga_tippspiel_actions\CommentAction;
use bundesliga_tippspiel_actions\DeleteCommentAction;
use bundesliga_tippspiel_comments\CommentBar;
use bundesliga_tippspiel_comments\CommentManager;

/**
 * Class DeleteCommentActionTest
 * Tests the DeleteCommentAction class
 */
class DeleteCommentActionTest extends TestClass {

	/**
	 * Tests deleting a comment
	 */
	public function testDeletingComment() {

		$_POST[CommentBar::$contentId] = "Hello World!";
		(new CommentAction())->execute();

		$commentManager = new CommentManager(self::$db);
		$_GET["comment"] = $commentManager->getComments()[0]->id;

		$this->assertEquals(count($commentManager->getComments()), 1);
		(new DeleteCommentAction())->execute();
		$this->assertEquals(count($commentManager->getComments()), 0);

	}

	/**
	 * Tests deleting the comment of another user, which should of course not
	 * be possible
	 */
	public function testDeletingOtherUsersComment() {

		$_POST[CommentBar::$contentId] = "Hello World!";
		(new CommentAction())->execute();

		$this->confirmedUserA->logout();
		$this->unConfirmedUserB->confirm(
			$this->unConfirmedUserB->confirmationToken);
		$this->unConfirmedUserB->login("B");

		$commentManager = new CommentManager(self::$db);
		$_GET["comment"] = $commentManager->getComments()[0]->id;

		$this->assertEquals(count($commentManager->getComments()), 1);
		(new DeleteCommentAction())->execute();
		$this->assertEquals(count($commentManager->getComments()), 1);
		$this->assertStatus("danger");
		$this->assertMessageId("COMMENT_DELETE_FAIL");

	}

	/**
	 * Tests deleting a comment without the user being logged in
	 */
	public function testDeletingCommentWithoutAuthentication() {

		$_POST[CommentBar::$contentId] = "Hello World!";
		(new CommentAction())->execute();

		$this->confirmedUserA->logout();

		$commentManager = new CommentManager(self::$db);
		$_GET["comment"] = $commentManager->getComments()[0]->id;

		$this->assertEquals(count($commentManager->getComments()), 1);
		(new DeleteCommentAction())->execute();
		$this->assertEquals(count($commentManager->getComments()), 1);
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

	}
}