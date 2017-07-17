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
use chameleon\LoginForm;
use welwitschi\Authenticator;

Functions::initializeSession();

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

