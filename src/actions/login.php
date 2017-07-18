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
use chameleon\LoginForm;
use ErrorException;
use welwitschi\Authenticator;

Functions::initializeSession();

/**
 * Logs a user in
 */
function login() {
	$username = $_POST[LoginForm::$username];
	$password = $_POST[LoginForm::$password];

	$auth = new Authenticator(Functions::getMysqli());
	$user = $auth->getUserFromUsername($username);

	if ($user !== null && $user->login($password)) {
		header('Location: ../index.php');
	} else {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{LOGIN_FAILED_MESSAGE_TITLE}",
			"body" => "@{LOGIN_FAILED_MESSAGE_BODY}"
		];
		header('Location: ../signup.php');
	}
}

// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	login();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
	throw $e;
}
