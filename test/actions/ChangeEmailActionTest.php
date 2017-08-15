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
use bundesliga_tippspiel_actions\ChangeEmailAction;
use chameleon\ChangeEmailForm;


/**
 * Class ChangeEmailActionTest
 * Test the ChangeEmailAction class
 */
class ChangeEmailActionTest extends TestClass {

	/**
	 * Tests changing an email address
	 * @SuppressWarnings checkUnusedVariables
	 */
	public function testSuccessfullyChangingEmailAddress() {
		$_POST[ChangeEmailForm::$newEmail] = "AA";
		(new ChangeEmailAction())->execute();
		$this->assertEquals($_SESSION["message"]["type"], "success");
		$this->assertNotNull(
			self::$authenticator->getUserFromEmailAddress("AA"));
	}

	/**
	 * Tests trying to change the email address with invalid login credentials
	 */
	public function testChangingEmailAddressWithInvalidAuthorization() {
		$_POST[ChangeEmailForm::$newEmail] = "AA";
		unset($_SESSION["user_id"]);

		(new ChangeEmailAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

		$_SESSION["user_id"] = -1;

		(new ChangeEmailAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

		$this->confirmedUserA->login("A");
		$this->confirmedUserA->logout();

		(new ChangeEmailAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

	}

	/**
	 * Tests trying to change the email address to an address that already
	 * exists
	 */
	public function testChangingToExistingEmailAddress() {
		$_POST[ChangeEmailForm::$newEmail] = "B";
		(new ChangeEmailAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("EMAIL_CHANGE_FAIL_DUPLICATE");
	}

	/**
	 * Tries to change the email address without providing input
	 */
	public function testChangingWithoutInput() {
		(new ChangeEmailAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("EMAIL_CHANGE_FAIL_NO_INPUT");
	}

}