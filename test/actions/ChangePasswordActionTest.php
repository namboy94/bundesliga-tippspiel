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
use bundesliga_tippspiel_actions\ChangePasswordAction;
use champlates\ChangePasswordForm;


/**
 * Class ChangePasswordActionTest
 * Tests the ChangePasswordAction class
 */
class ChangePasswordActionTest extends TestClass {

	/**
	 * Tests changing the password without input
	 */
	public function testWithoutInput() {
		(new ChangePasswordAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("PASSWORD_CHANGE_FAIL_MISSING_INPUT");
	}

	/**
	 * Tests using invalid new password input
	 */
	public function testWithInvalidNewPasswordInput() {
		$_POST[ChangePasswordForm::$oldPassword] = "A";
		$_POST[ChangePasswordForm::$newPassword] = "BBBB";
		$_POST[ChangePasswordForm::$newPasswordRepeat] = "AAA";

		(new ChangePasswordAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("PASSWORD_REPEAT_NO_MATCH_SHORT");

		$_POST[ChangePasswordForm::$newPassword] = "AAA";

		(new ChangePasswordAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("PASSWORD_TOO_SHORT");
	}

	/**
	 * Tests ussing invalid old password
	 */
	public function testWithWrongOldPassword() {
		$_POST[ChangePasswordForm::$oldPassword] = "B";
		$_POST[ChangePasswordForm::$newPassword] = "BBBB";
		$_POST[ChangePasswordForm::$newPasswordRepeat] = "BBBB";

		(new ChangePasswordAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("PASSWORD_CHANGE_FAIL_OLD_PASSWORD");
	}

	/**
	 * Tests a successful password change
	 */
	public function testSuccessfulPasswordChange() {
		$_POST[ChangePasswordForm::$oldPassword] = "A";
		$_POST[ChangePasswordForm::$newPassword] = "BBBB";
		$_POST[ChangePasswordForm::$newPasswordRepeat] = "BBBB";
		(new ChangePasswordAction())->execute();
		$this->assertStatus("success");
	}

	/**
	 * Tests changing a password as an unauthenticated user
	 */
	public function testChangingPasswordAsUnauthorizedUser() {

		$this->confirmedUserA->logout();
		$_POST[ChangePasswordForm::$oldPassword] = "A";
		$_POST[ChangePasswordForm::$newPassword] = "BBBB";
		$_POST[ChangePasswordForm::$newPasswordRepeat] = "BBBB";
		(new ChangePasswordAction())->execute();

		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");

		$this->unConfirmedUserB->confirm(
			$this->unConfirmedUserB->confirmationToken);
		$this->confirmedUserA->login("A");
		$_SESSION["user_id"] = $this->unConfirmedUserB->id;

		$_POST[ChangePasswordForm::$oldPassword] = "A";
		$_POST[ChangePasswordForm::$newPassword] = "BBBB";
		$_POST[ChangePasswordForm::$newPasswordRepeat] = "BBBB";
		(new ChangePasswordAction())->execute();

		$this->assertStatus("danger");
		$this->assertMessageId("ACTION_FAIL_AUTH");
	}
}