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
use bundesliga_tippspiel\Functions;
use chameleon\ChangeUsernameForm;
use welwitschi\Authenticator;


/**
 * Class ChangeUsernameAction
 * Allows users to change their usernames
 * @package bundesliga_tippspiel_actions
 */
class ChangeUsernameAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: An ActionExpression containing message data
	 */
	protected function defineBehaviour() {

		if (!isset($_POST[ChangeUsernameForm::$newUsername])) {
			throw new DangerException("USERNAME_CHANGE_FAIL_NO_INPUT",
				"../profile.php");
		}

		$newUsername = $_POST[ChangeUsernameForm::$newUsername];

		if ($newUsername === "" || strlen($newUsername) > 10) {
			throw new DangerException("USERNAME_CHANGE_FAIL_USERNAME",
				"../profile.php");
		}

		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($_SESSION["user_id"]);

		if ($user->changeUsername($newUsername)) {
			throw new SuccessException("USERNAME_CHANGE_SUCCESS",
				"../profile.php");

		} else {
			throw new DangerException("USERNAME_CHANGE_FAIL_DUPLICATE",
				"../profile.php");
		}
	}
}