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
use chameleon\ChangePasswordForm;
use welwitschi\Authenticator;


/**
 * Class ChangePasswordAction
 * Changes the password of a user
 * @package bundesliga_tippspiel_actions
 */
class ChangePasswordAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: An ActionExpression containing message data
	 */
	protected function defineBehaviour() {

		foreach ([ChangePasswordForm::$oldPassword,
					ChangePasswordForm::$newPassword,
					ChangePasswordForm::$newPasswordRepeat] as $value) {
			if (!isset($_POST[$value])) {
				throw new DangerException("PASSWORD_CHANGE_FAIL_MISSING_INPUT",
					"../profile.php");
			}
		}

		$oldPassword = $_POST[ChangePasswordForm::$oldPassword];
		$newPassword = $_POST[ChangePasswordForm::$newPassword];
		$newPasswordRepeat = $_POST[ChangePasswordForm::$newPasswordRepeat];

		SignupAction::validatePassword($newPassword, $newPasswordRepeat);

		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($_SESSION["user_id"]);

		if ($user->changePassword($oldPassword, $newPassword)) {
			throw new SuccessException("PASSWORD_CHANGE_SUCCESS",
				"../profile.php");
		} else {
			throw new DangerException("PASSWORD_CHANGE_FAIL_OLD_PASSWORD",
				"../profile.php");
		}
	}
}