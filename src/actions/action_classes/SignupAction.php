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

namespace bundesliga_tippspiel_actions;
use bundesliga_tippspiel\DefaultDictionary;
use bundesliga_tippspiel\Functions;
use champlates\FormReCaptcha;
use champlates\SignupForm;
use welwitschi\Authenticator;


/**
 * Class SignupAction
 * Handles the Signup for a user
 * @package bundesliga_tippspiel_actions
 */
class SignupAction extends Action {

	/**
	 * SignupAction constructor.
	 * @param bool $authenticationRequired: Set to false since signup does
	 *                                      not require login
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: An ActionExpression containing message data
	 */
	protected function defineBehaviour() {

		$auth = new Authenticator($this->db);
		$dict = new DefaultDictionary();

		$username = $_POST[SignupForm::$username];
		$email = $_POST[SignupForm::$email];
		$password = $_POST[SignupForm::$password];
		$passwordRepeat = $_POST[SignupForm::$passwordRepeat];
		$captcha = $_POST[FormReCaptcha::$recaptchaPostKey];

		if ($password !== $passwordRepeat) {
			throw new DangerException(
				"SIGNUP_FAILED_PASSWORD_MATCH", "../signup.php");

		} elseif (strlen($password) < 4) {
			throw new DangerException(
				"SIGNUP_FAILED_PASSWORD_TOO_SHORT", "../signup.php");

		} elseif ($username === "" || strlen($username) > 10) {
			throw new DangerException(
				"SIGNUP_FAILED_USERNAME", "../signup.php");

		} elseif ($_SERVER["SERVER_NAME"] !== "localhost"
			&& !Functions::verifyCaptcha($captcha)) {
			// Check Captcha in production but not on localhost

			// @codeCoverageIgnoreStart
			throw new DangerException(
				"SIGNUP_FAILED_RECAPTCHA", "../signup.php");
			// @codeCoverageIgnoreEnd

		} elseif ($auth->createUser($username, $email, $password)) {

			$user = $auth->getUserFromUsername($username);

			$server = $_SERVER["SERVER_NAME"] . ":" . $_SERVER["SERVER_PORT"];
			$confirmationUrl = "https://" . $server . "/actions/confirm.php";
			$confirmationUrl .= "?id=" . $user->id . "&token=";
			$confirmationUrl .= $user->confirmationToken;

			// Send an email to the user's email address with the confirmation
			// URL
			mail(
				$email,
				$dict->translate("@{SIGNUP_EMAIL_TITLE}",
					Functions::getLanguage()),
				$dict->translate("@{SIGNUP_EMAIL_BODY_START}\n\n" .
					$confirmationUrl . "\n\n@{SIGNUP_EMAIL_BODY_END}",
					Functions::getLanguage()));

			throw new SuccessException("SIGNUP_SUCCESS", "../signup.php");

		} else {
			throw new DangerException("SIGNUP_FAILED", "../signup.php");
		}
	}

	/**
	 * Validates a password
	 * @param string $password: The password to validate
	 * @param string $repeat: The password repeat/confirmation
	 * @throws ActionException: If the password is invalid
	 */
	public static function validatePassword(string $password, string $repeat) {

		$redirect = $_SERVER["HTTP_REFERER"];

		if (strlen($password) < 4) {
			throw new DangerException("PASSWORD_TOO_SHORT", $redirect);

		} elseif ($password !== $repeat) {
			throw new DangerException("PASSWORD_REPEAT_NO_MATCH_SHORT",
				$redirect);
		}

	}
}