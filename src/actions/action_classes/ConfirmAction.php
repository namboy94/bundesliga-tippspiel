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
use welwitschi\Authenticator;


/**
 * Class ConfirmAction
 * Enables the user to confirm their account
 * @package bundesliga_tippspiel_actions
 */
class ConfirmAction extends Action {

	/**
	 * ConfirmAction constructor.
	 * @param bool $authenticationRequired: Set to false since confirming does
	 *                                      not require login
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

		if (!isset($_GET["id"]) || !isset($_GET["token"])) {
			throw new DangerException("CONFIRM_FAILED_NO_INPUT",
				"../index.php");
		}

		$id = $_GET["id"];
		$token = $_GET["token"];

		$auth = new Authenticator($this->db);
		$user = $auth->getUserFromId($id);

		if ($user === null || !$user->confirm($token)) {
			throw new DangerException("CONFIRM_FAILED", "../index.php");

		} else {
			throw new SuccessException("CONFIRM_SUCCESS", "../index.php");
		}
	}
}