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

namespace bundesliga_tippspiel;
require __DIR__ . '/../../vendor/autoload.php';
use chameleon\ForgottenPasswordForm;
use chameleon\FormReCaptcha;
use welwitschi\Authenticator;
use ErrorException;

/**
 * The password_reset() action resets a user's password.
 * This will only succeed if the user provides a valid email
 * address and successfully filled in the ReCaptcha form.
 * If an email is provided that does not exist in the database we
 * still tell the user that the password reset was a suggest to make it
 * harder to tell which email addresses have accounts on our website
 */
function password_reset() {

	Functions::initializeSession();

	$email = $_POST[ForgottenPasswordForm::$email];
	$recaptcha = $_POST[FormReCaptcha::$recaptchaPostKey];

	if ($_SERVER["SERVER_NAME"] !== "localhost"
		&& !Functions::verifyCaptcha($recaptcha)) {

		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{RESET_PASSWORD_ERROR_RECAPTCHA_TITLE}",
			"body" => "@{RESET_PASSWORD_ERROR_RECAPTCHA_BODY}"
		];
		header("Location: ../forgot.php");

	} else {

		$dict = new DefaultDictionary();
		$auth = new Authenticator(Functions::getMysqli());
		$user = $auth->getUserFromEmailAddress($email);
		if ($user !== null) {
			$password = $user->resetPassword();
			mail($email,
				$dict->translate("@{PASSWORD_RESET_EMAIL_TITLE}", "en"),
				$dict->translate("@{PASSWORD_RESET_EMAIL_BODY_START}\n\n" .
					$password . "\n\n@{PASSWORD_RESET_EMAIL_BODY_END}", "en"));
		}

		$_SESSION["message"] = [
			"type" => "success",
			"title" => "@{RESET_PASSWORD_SUCCESS_TITLE}",
			"body" => "@{RESET_PASSWORD_SUCCESS_BODY}"
		];
		header("Location: ../index.php");
	}
}


// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline ){
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	password_reset();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
}