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
use bundesliga_tippspiel_actions\SignupAction;
use chameleon\FormReCaptcha;
use chameleon\SignupForm;

/**
 * Class SignupActionTest
 * Tests the SignupAction class
 */
class SignupActionTest extends TestClass {

	/**
	 * Tests creating a new user
	 */
	public function testCreatingNewUser() {

		$user = self::$authenticator->getUserFromUsername("Z");
		$this->assertNull($user);

		$_POST[SignupForm::$username] = "Z";
		$_POST[SignupForm::$email] = "Z";
		$_POST[SignupForm::$password] = "ZZZZ";
		$_POST[SignupForm::$passwordRepeat] = "ZZZZ";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		$_SERVER["SERVER_PORT"] = 80; // Why do I have to set this manually?
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromUsername("Z");
		$this->assertNotNull($user);
		$this->assertFalse($user->confirmed);

		$this->assertStatus("success");
		$this->assertMessageId("SIGNUP_SUCCESS");

	}

	/**
	 * Tests creating a user that already exists
	 */
	public function testCreatingExisting() {

		$_POST[SignupForm::$username] = "A";
		$_POST[SignupForm::$email] = "Z";
		$_POST[SignupForm::$password] = "ZZZZ";
		$_POST[SignupForm::$passwordRepeat] = "ZZZZ";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromEmailAddress("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED");

		$_POST[SignupForm::$username] = "Z";
		$_POST[SignupForm::$email] = "A";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromUsername("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED");

	}

	/**
	 * Tests creating a new user using a password that's too short
	 */
	public function testPasswordTooShort() {

		$_POST[SignupForm::$username] = "Z";
		$_POST[SignupForm::$email] = "Z";
		$_POST[SignupForm::$password] = "ZZZ";
		$_POST[SignupForm::$passwordRepeat] = "ZZZ";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromEmailAddress("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED_PASSWORD_TOO_SHORT");

	}

	/**
	 * Tests creating a new user but with two differing passwords
	 */
	public function testPasswordMissmatch() {

		$_POST[SignupForm::$username] = "Z";
		$_POST[SignupForm::$email] = "Z";
		$_POST[SignupForm::$password] = "ZZZZZ";
		$_POST[SignupForm::$passwordRepeat] = "ZZZZ";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromEmailAddress("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED_PASSWORD_MATCH");

	}

	/**
	 * Tests creating a new user using an invalid username
	 */
	public function testInvalidUsername() {

		$_POST[SignupForm::$username] = "";
		$_POST[SignupForm::$email] = "Z";
		$_POST[SignupForm::$password] = "ZZZZ";
		$_POST[SignupForm::$passwordRepeat] = "ZZZZ";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromEmailAddress("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED_USERNAME");

		$_POST[SignupForm::$username] = "ZZZZZZZZZZZ";
		(new SignupAction())->execute();

		$user = self::$authenticator->getUserFromEmailAddress("Z");
		$this->assertNull($user);

		$this->assertStatus("danger");
		$this->assertMessageId("SIGNUP_FAILED_USERNAME");

	}

}
