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

namespace bundesliga_tippspiel_actions;
require __DIR__ . '/../../vendor/autoload.php';
use bundesliga_tippspiel\Functions;
use bundesliga_tippspiel\DefaultDictionary;
use chameleon\FormReCaptcha;
use ErrorException;
use chameleon\SignupForm;
use welwitschi\Authenticator;

Functions::initializeSession();

/**
 * Signs a user up
 */
function signup() {
	$auth = new Authenticator(Functions::getMysqli());
	$dict = new DefaultDictionary();

	$username = $_POST[SignupForm::$username];
	$email = $_POST[SignupForm::$email];
	$password = $_POST[SignupForm::$password];
	$passwordRepeat = $_POST[SignupForm::$passwordRepeat];
	$captcha = $_POST[FormReCaptcha::$recaptchaPostKey];

	if ($password !== $passwordRepeat) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{SIGNUP_FAILED_PASSWORD_MATCH_MESSAGE_TITLE}",
			"body" => "@{SIGNUP_FAILED_PASSWORD_MATCH_MESSAGE_BODY}"
		];

		// Check Captcha in production but not on localhost
	} elseif ($_SERVER["SERVER_NAME"] !== "localhost"
		&& !Functions::verifyCaptcha($captcha)) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{SIGNUP_FAILED_RECAPTCHA_MESSAGE_TITLE}",
			"body" => "@{SIGNUP_FAILED_RECAPTCHA_MESSAGE_BODY}"
		];

	} elseif ($auth->createUser($username, $email, $password)) {
		$user = $auth->getUserFromUsername($username);

		$server = $_SERVER["SERVER_NAME"] . ":" . $_SERVER["SERVER_PORT"];
		$confirmationUrl = "https://" . $server . "/actions/confirm.php?id=";
		$confirmationUrl .= $user->id . "&token=" . $user->confirmationToken;

		mail(
			$email,
			$dict->translate("@{SIGNUP_EMAIL_TITLE}", "en"),
			$dict->translate("@{SIGNUP_EMAIL_BODY_START}\n\n" .
				$confirmationUrl . "\n\n@{SIGNUP_EMAIL_BODY_END}", "en"));

		$_SESSION["message"] = [
			"type" => "success",
			"title" => "@{SIGNUP_SUCCESS_MESSAGE_TITLE}",
			"body" => "@{SIGNUP_SUCCESS_MESSAGE_BODY}"
		];

	} else {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{SIGNUP_FAILED_MESSAGE_TITLE}",
			"body" => "@{SIGNUP_FAILED_MESSAGE_BODY}"
		];
	}

	header('Location: ../signup.php');
}

// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	signup();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
	throw $e;
}