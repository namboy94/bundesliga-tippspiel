<?php
/**
 * Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>
 *
 * This file is part of bundesliga-tippspiel.
 *
 * bundesliga-tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga-tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga-tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel_actions;
use function bundesliga_tippspiel_kudubot_communication\deRegister;
use function bundesliga_tippspiel_kudubot_communication\isValidConnection;
use welwitschi\Authenticator;

/**
 * Class RegisterReminderAction
 * De-registers a kudubot reminder
 * @package bundesliga_tippspiel_actions
 */
class UnRegisterReminderAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: The message information
	 */
	protected function defineBehaviour() {

		$auth = new Authenticator($this->db);
		if (isset($_SESSION["user_id"])) {
			$user = $auth->getUserFromId($_SESSION["user_id"]);
			if ($user !== null &&
				$user->isLoggedIn() &&
				isset($_GET["connection"])) {

				$connection = $_GET["connection"];

				if (!isValidConnection($connection)) {
					throw new RedirectException("../index.php");
				} else {
					deRegister(
						$user->id,
						$connection
					);
				}


			} else {
				throw new RedirectException("../index.php");
			}
		}
	}
}