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
use bundesliga_tippspiel_actions\ChangePasswordAction;
use chameleon\ChangePasswordForm;


/**
 * Class ChangePasswordActionTest
 * Tests the ChangePasswordAction class
 */
class ChangePasswordActionTest extends TestClass {

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
}