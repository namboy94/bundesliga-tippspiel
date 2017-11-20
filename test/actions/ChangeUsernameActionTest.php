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
use bundesliga_tippspiel_actions\ChangeUsernameAction;
use champlates\ChangeUsernameForm;


/**
 * Class ChangeUsernameActionTest
 * Tests the ChangeUsernameAction class
 */
class ChangeUsernameActionTest extends TestClass {

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

	/**
	 * Tests changing the username to an existing username
	 */
	public function testDuplicateUsername() {
		$_POST[ChangeUsernameForm::$newUsername] = "B";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("USERNAME_CHANGE_FAIL_DUPLICATE");
	}

	/**
	 * Tests a successful username change
	 */
	public function testSuccessfulUsernameChange() {
		$_POST[ChangeUsernameForm::$newUsername] = "C";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("success");
	}

	/**
	 * Tests if it is possible to change the username of another user.
	 * Hint: This should not be possible
	 */
	public function testChangingOtherUsersUsername() {

		$this->confirmedUserA->logout();

		$_POST[ChangeUsernameForm::$newUsername] = "C";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

		$this->unConfirmedUserB->confirm(
			$this->unConfirmedUserB->confirmationToken);
		$this->confirmedUserA->login("A");
		$_SESSION["user_id"] = $this->unConfirmedUserB->id;

		$_POST[ChangeUsernameForm::$newUsername] = "C";
		(new ChangeUsernameAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

	}

}