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
use bundesliga_tippspiel_actions\CommentAction;
use bundesliga_tippspiel_comments\CommentBar;


/**
 * Class CommentActionTest
 * Tests the CommentAction class
 */
class CommentActionTest extends TestClass {

	/**
	 * Tests commenting without providing input
	 */
	public function testCommentingWithoutInput() {
		$this->assertEquals(count(self::$commentManager->getComments()), 0);
		(new CommentAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("COMMENT_FAIL_NO_INPUT");
		$this->assertEquals(count(self::$commentManager->getComments()), 0);
	}

	/**
	 * Tests placing a comment
	 * @SuppressWarnings checkUnusedVariables
	 */
	public function testPlacingComment() {
		$this->assertEquals(count(self::$commentManager->getComments()), 0);
		$_POST[CommentBar::$contentId] = "Hello World!";
		(new CommentAction())->execute();
		$this->assertTrue(!isset($_SESSION["message"]));
		$this->assertEquals(count(self::$commentManager->getComments()), 1);
	}

	/**
	 * Tests placing comments as an unauthorized user
	 */
	public function testPlacingCommentWithoutAuthorization() {
		$this->confirmedUserA->logout();

		$this->assertEquals(count(self::$commentManager->getComments()), 0);
		$_POST[CommentBar::$contentId] = "Hello World!";
		(new CommentAction())->execute();

		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");
		$this->assertEquals(count(self::$commentManager->getComments()), 0);
	}

	/**
	 * Tests placing an empty comment
	 */
	public function testEmptyComment() {

		$this->assertEquals(count(self::$commentManager->getComments()), 0);
		$_POST[CommentBar::$contentId] = "";
		(new CommentAction())->execute();

		$this->assertStatus("danger");
		$this->assertMessageId("COMMENT_FAIL_EMPTY_INPUT");
		$this->assertEquals(count(self::$commentManager->getComments()), 0);

	}
}