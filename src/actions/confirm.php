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
use welwitschi\Authenticator;
use ErrorException;
use bundesliga_tippspiel\Functions;

Functions::initializeSession();

/**
 * Confirms a newly created user
 */
function confirm() {
	$auth = new Authenticator(Functions::getMysqli());

	$id = $_GET["id"];
	$token = $_GET["token"];
	$user = $auth->getUserFromId($id);

	if ($user === null || !$user->confirm($token)) {
		$_SESSION["message"] = [
			"type" => "danger",
			"title" => "@{CONFIRM_FAILED_MESSAGE_TITLE}",
			"body" => "@{CONFIRM_FAILED_MESSAGE_BODY}"
		];
	} else {
		$_SESSION["message"] = [
			"type" => "success",
			"title" => "@{CONFIRM_SUCCESS_MESSAGE_TITLE}",
			"body" => "@{CONFIRM_SUCCESS_MESSAGE_BODY}"
		];
	}
	header("Location: ../index.php");
}

// Make ErrorException catch everything
set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	confirm();
} catch (ErrorException $e) {
	echo "Oops... Something broke on our end, sorry!";
	throw $e;
}