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
use bundesliga_tippspiel_actions\ChangeUsernameAction;
use chameleon\ChangeUsernameForm;


/**
 * Class ChangeUsernameActionTest
 * Tests the ChangeUsernameAction class
 */
class ChangeUsernameActionTest extends TestClass {

	/**
	 * Don't Fetch data beforehand
	 * @param bool $fetchMatchData: false
	 * @SuppressWarnings checkUnusedFunctionParameters
	 */
	public static function setUpBeforeClass(bool $fetchMatchData = false) {
		parent::setUpBeforeClass($fetchMatchData);
	}

	/**
	 * Tests changing the password without input
	 */
	public function testWithoutInput() {
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("USERNAME_CHANGE_FAIL_NO_INPUT");
	}

	/**
	 * Tests setting the username to an invalid value
	 */
	public function testInvalidUsername() {
		$_POST[ChangeUsernameForm::$newUsername] = "";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("USERNAME_CHANGE_FAIL_USERNAME");

		$_POST[ChangeUsernameForm::$newUsername] = "12345678901";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("USERNAME_CHANGE_FAIL_USERNAME");
	}

	public function testDuplicateUsername() {
		$_POST[ChangeUsernameForm::$newUsername] = "B";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("USERNAME_CHANGE_FAIL_DUPLICATE");
	}

	public function testSuccessfulUsernameChange() {
		$_POST[ChangeUsernameForm::$newUsername] = "C";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("success");
	}

}