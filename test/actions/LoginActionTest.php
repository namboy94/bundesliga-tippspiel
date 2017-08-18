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
use bundesliga_tippspiel_actions\LoginAction;
use chameleon\LoginForm;

/**
 * Class LoginActionTest
 * Tests the LoginAction class
 */
class LoginActionTest extends TestClass {

	/**
	 * Tests if the Login Action successfully logs the user in
	 */
	public function testSuccessfullyLoggingIn() {
		$this->confirmedUserA->logout();
		$_POST[LoginForm::$username] = "A";
		$_POST[LoginForm::$password] = "A";
		(new LoginAction())->execute();

		$this->assertTrue(
			self::$authenticator->getUserFromUsername("A")->isLoggedIn());
	}

	/**
	 * Tests Logging in with an incorrect password
	 */
	public function testLoggingInWithWrongPassword() {

		$this->confirmedUserA->logout();
		$_POST[LoginForm::$username] = "A";
		$_POST[LoginForm::$password] = "B";
		(new LoginAction())->execute();

		$this->assertFalse(
			self::$authenticator->getUserFromUsername("A")->isLoggedIn());
		$this->assertStatus("danger");
		$this->assertMessageId("LOGIN_FAILED");

	}

	/**
	 * Tests trying to log in using a username that does not exist
	 */
	public function testLoggingInWithNonExistantUser() {

		$this->confirmedUserA->logout();
		$_POST[LoginForm::$username] = "Z";
		$_POST[LoginForm::$password] = "Z";
		(new LoginAction())->execute();

		$this->assertFalse(isset($_SESSION["user_id"]));
		$this->assertFalse(isset($_SESSION["authentication_token"]));
		$this->assertStatus("danger");
		$this->assertMessageId("LOGIN_FAILED");

	}

}
