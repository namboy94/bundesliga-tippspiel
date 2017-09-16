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
use chameleon\LoginForm;
use welwitschi\Authenticator;

/**
 * Class LoginAction
 * Enables the user to log in
 * @package bundesliga_tippspiel_actions
 */
class LoginAction extends Action {

	/**
	 * LoginAction constructor.
	 * @param bool $authenticationRequired: Set to false since logging in does
	 *                                      not require the user to already be
	 *                                      logged in
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: The message information
	 */
	protected function defineBehaviour() {

		$username = $_POST[LoginForm::$username];
		$password = $_POST[LoginForm::$password];

		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromUsername($username);

		if ($user !== null && $user->login($password)) {
			throw new RedirectException("../index.php");
			// header('Location: ../index.php');
		} else {
			throw new DangerException("LOGIN_FAILED", "../signup.php");
		}
	}
}