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
use chameleon\ChangePasswordForm;
use welwitschi\Authenticator;
use ErrorException;

/**
 * Change The Password of a logged in user
 */
function changePassword() {

	Functions::initializeSession();

	$oldPassword = $_POST[ChangePasswordForm::$oldPassword];
	$newPassword = $_POST[ChangePasswordForm::$newPassword];
	$newPasswordRepeat = $_POST[ChangePasswordForm::$newPasswordRepeat];

	if ($newPassword !== $newPasswordRepeat) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{PASSWORD_CHANGE_FAIL_PASSWORD_MATCH_TITLE}",
			"body" => "@{PASSWORD_CHANGE_FAIL_PASSWORD_MATCH_BODY}"
		];
		header("Location: ../profile.php");

	} elseif (strlen($newPassword) < 5) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{PASSWORD_CHANGE_FAIL_PASSWORD_LENGTH_TITLE}",
			"body" => "@{PASSWORD_CHANGE_FAIL_PASSWORD_LENGTH_BODY}"
		];
		header("Location: ../profile.php");

	} elseif (isset($_SESSION["user_id"])) {
		$auth = new Authenticator(Functions::getMysqli());
		$user = $auth->getUserFromId($_SESSION["user_id"]);
		if ($user !== null) {
			if ($user->changePassword($oldPassword, $newPassword)) {
				$_SESSION["message"] = [
					"type" => "success",
					"title" => "@{PASSWORD_CHANGE_SUCCESS_TITLE}",
					"body" => "@{PASSWORD_CHANGE_SUCCESS_BODY}"
				];
			} else {
				$_SESSION["message"] = [
					"type" => "danger",
					"title" => "@{PASSWORD_CHANGE_FAIL_OLD_PASSWORD_TITLE}",
					"body" => "@{PASSWORD_CHANGE_FAIL_OLD_PASSWORD_BODY}"
				];
			}
			header("Location: ../profile.php");
		} else {
			// Not a logged in user, go back to Home!
			header("Location: ../index.php");
		}
	} else {
		// Not a logged in user, go back to Home!
		header("Location: ../index.php");
	}
}


// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	changePassword();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
	throw $e;
}