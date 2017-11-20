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
use bundesliga_tippspiel_actions\PasswordResetAction;
use chameleon\ForgottenPasswordForm;
use chameleon\FormReCaptcha;

/**
 * Class PasswordResetActionTest
 * Tests the PasswordResetAction class
 */
class PasswordResetActionTest extends TestClass {

	/**
	 * Tests resetting a password
	 */
	public function testResettingPassword() {

		$oldHash = $this->confirmedUserA->pwHash;

		/**
		 * @SuppressWarnings checkUnusedVariables
		 */
		$_POST[ForgottenPasswordForm::$email] = "A";
		$_POST[FormReCaptcha::$recaptchaPostKey] = "";
		(new PasswordResetAction())->execute();

		$newHash = self::$authenticator->getUserFromEmailAddress("A")->pwHash;
		$this->assertNotEquals($oldHash, $newHash);
	}

}
