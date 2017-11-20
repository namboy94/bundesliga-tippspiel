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
 * Class RedirectException
 * Simple class that allows redirecting to another page
 * @package bundesliga_tippspiel_actions
 */
class RedirectException extends ActionException {

	/**
	 * RedirectException constructor.
	 * @param string $redirectLocation: The Location to redirect to
	 */
	public function __construct(string $redirectLocation) {
		parent::__construct("", "", $redirectLocation);
	}

	/**
	 * Does not store a message in the session,
	 * since this is a simple redirect
	 */
	public function storeMessageInSession() {
		// NoOp
	}

}