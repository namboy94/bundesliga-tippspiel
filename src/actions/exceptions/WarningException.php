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


/**
 * Class WarningException
 * ActionException subclass that automatically sets
 * the message type to 'warning'.
 * @package bundesliga_tippspiel_actions
 */
class WarningException extends ActionException {

	/**
	 * WarningException constructor.
	 * Overrides the standard ActionException constructor to automatically
	 * set the message type to 'warning'
	 * @param string $messageIdentifier: The identifier for the message
	 * @param string $redirect: The site to redirect to
	 */
	public function __construct(string $messageIdentifier, string $redirect) {
		parent::__construct($messageIdentifier, "warning", $redirect);
	}
}