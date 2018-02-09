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
use bundesliga_tippspiel\DefaultDictionary;
use bundesliga_tippspiel\Functions;
use bundesliga_tippspiel_kudubot_communication\KudubotCommunication;
use welwitschi\Authenticator;

/**
 * Class RegisterReminderAction
 * Registers a kudubot reminder
 * @package bundesliga_tippspiel_actions
 */
class RegisterReminderAction extends Action {

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: The message information
	 */
	protected function defineBehaviour() {

		$auth = new Authenticator($this->db);
		$dict = new DefaultDictionary();

		if (isset($_SESSION["user_id"])) {
			$user = $auth->getUserFromId($_SESSION["user_id"]);
			if ($user !== null && 
				$user->isLoggedIn() && 
				isset($_GET["warning_time"])&& 
				isset($_GET["connection"])) {

				$warningTime = (int)$_GET["warning_time"];
				$connection = $_GET["connection"];


				if (!KudubotCommunication::isValidConnection($connection)) {
					throw new DangerException(
						"KUDUBOT_REGISTRATION_INVALID_CONNECTION",
						"../profile.php"
					);
					// thomas was here
				} else {
					$key = KudubotCommunication::register(
						$user->id,
						$user->username,
						$connection,
						$warningTime
					);

					$address = "OK";
					mail(
						$user->email,
						$dict->translate(
							"@{KUDUBOT_REGISTRATION_EMAIL_TITLE}",
							Functions::getLanguage()
						),
						$dict->translate(
							"@{KUDUBOT_REGISTRATION_EMAIL_BODY_START}\n\n" .
							"/register " . $key . "\n\n" .
							"@{KUDUBOT_REGISTRATION_EMAIL_BODY_MIDDLE}\n\n" .
							$address . "\n\n" .
							"@{KUDUBOT_REGISTRATION_EMAIL_BODY_END}",
							Functions::getLanguage()
						)
					);

					throw new InfoException(
						"KUDUBOT_REGISTRATION_EMAIL_NOTICE",
						"../profile.php"
					);
				}

			} else {
				throw new DangerException(
					"KUDUBOT_REGISTRATION_AUTH_FAIL",
					"../profile.php"
				);
			}
		}
	}
}