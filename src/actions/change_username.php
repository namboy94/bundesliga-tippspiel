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
use chameleon\ChangeUsernameForm;
use welwitschi\Authenticator;
use ErrorException;

/**
 * Changes the username of a logged in user
 */
function change_username() {

	Functions::initializeSession();

	$newUsername = $_POST[ChangeUsernameForm::$newUsername];

	if (isset($_SESSION["user_id"])) {
		$auth = new Authenticator(Functions::getMysqli());
		$user = $auth->getUserFromId($_SESSION["user_id"]);
		if ($user !== null) {
			if (!$user->isLoggedIn()) {
				$_SESSION["message"] = [
					"type" => "danger",
					"title" => "@{USERNAME_CHANGE_FAIL_LOGIN_AUTH_TITLE}",
					"body" => "@{USERNAME_CHANGE_FAIL_LOGIN_AUTH_BODY}"
				];
				header("Location: ../index.php");
			} elseif ($user->changeUsername($newUsername)) {
				$_SESSION["message"] = [
					"type" => "success",
					"title" => "@{USERNAME_CHANGE_SUCCESS_TITLE}",
					"body" => "@{USERNAME_CHANGE_SUCCESS_BODY}"
				];
				header("Location: ../profile.php");
			} else {
				$_SESSION["message"] = [
					"type" => "danger",
					"title" => "@{USERNAME_CHANGE_FAIL_DUPLICATE_TITLE}",
					"body" => "@{USERNAME_CHANGE_FAIL_DUPLICATE_BODY}"
				];
				header("Location: ../profile.php");
			}

		} else {
			header("Location: ../index.php");
		}
	} else {
		header("Location: ../index.php");
	}
	header("Location: ../profile.php");

}


// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline ){
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	change_username();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
}