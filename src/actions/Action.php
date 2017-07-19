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
use Exception;


/**
 * Class Action
 * Class that offers a general framework for actions
 * @package bundesliga_tippspiel_actions
 */
abstract class Action {

	/**
	 * Action constructor.
	 */
	public function __construct() {
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 */
	protected abstract function defineBehaviour();

	/**
	 * Executes the action behaviour. Listens for (expected) ActionExceptions
	 * and handles their messages and redirects. If the defineBehaviour()
	 * method does not throw one of these Exceptions, a redirect header will
	 * be set to the previous page. This will however be ignored in case
	 * a header location was previously set.
	 * If an unexpected error occurs, the user will be informed and the
	 * Exception will be re-thrown to be logged by the system
	 * @throws Exception: The re-thrown unexpected Exception
	 */
	protected function execute() {

		try {
			$this->defineBehaviour();
			// If no header(Location...) was set beforehand, just return
			// to the previous page
			header("Location: " . $_SERVER["HTTP_REFERER"]);

		} catch (ActionException $e) {
			$e->storeMessageInSession();
			$e->setHeaderToRedirect();

		} catch (Exception $e) {
			echo "Oops... Something broke on our end, sorry!";
			throw $e;
		}
	}
}