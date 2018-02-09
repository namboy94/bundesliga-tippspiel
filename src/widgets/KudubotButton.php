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

namespace bundesliga_tippspiel;
require __DIR__ . '/../../vendor/autoload.php';
use bundesliga_tippspiel_kudubot_communication\KudubotCommunication;
use champlates\HtmlTemplate;

/**
 * Class KudubotButton
 * Class that models a button to activate or de-activate a kudubot reminder
 * @package bundesliga_tippspiel
 */
class KudubotButton extends HtmlTemplate {

	/**
	 * KudubotButton constructor.
	 * @param int $user_id: The logged in user's ID
	 * @param string $connection: The kudubot connection to use
	 *                            (whatsapp, telegram etc.)
	 */
	public function __construct(int $user_id, string $connection) {

		parent::__construct(
			__DIR__ . "/templates/kudubot_button.html", null
		);

		$active = KudubotCommunication::getRegisteredStatus(
			$user_id, $connection
		);

		if ($active) {
			$action = "unregister_reminder";
			$state = "active";
		} else {
			$action = "register_reminder";
			$state = "inactive";
		}

		if ($connection === "whatsapp") {
			$logo = "https://upload.wikimedia.org/wikipedia/commons/6/6b/" .
				"WhatsApp.svg";
		} elseif ($connection === "telegram") {
			$logo = "https://upload.wikimedia.org/wikipedia/commons/8/82/" .
				"Telegram_logo.svg";
		} else {
			$logo = "";
		}

		$this->bindParams([
			"ACTION" => $action,
			"CONNECTION" => $connection,
			"STATE" => $state,
			"LOGO" => $logo,
			"WARNING_TIME" => "600"
		]);
	}
}
