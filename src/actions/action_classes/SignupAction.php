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
	public function __construct($authenticationRequired = false){
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: An ActionExpression containing message data
	 */
	protected function defineBehaviour(){

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