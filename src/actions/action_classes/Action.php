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
use bundesliga_tippspiel\Functions;
use Exception;
use welwitschi\Authenticator;


/**
 * Class Action
 * Class that offers a general framework for actions
 * @package bundesliga_tippspiel_actions
 */
abstract class Action {

	/**
	 * Action constructor.
	 * @param bool $authenticationRequired: Can be set to false to allow
	 *                                      user to use the action without
	 *                                      being logged in.
	 */
	public function __construct(bool $authenticationRequired = true) {
		Functions::initializeSession();
		$this->db = Functions::getMysqli();
		$this->authenticationRequired = $authenticationRequired;
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
	 * Exception will be re-thrown to be logged by the system.
	 *
	 * This method also checks if a user is authenticated for actions that
	 * require user authentication, which can be set using the
	 * authenticationRequired variable.
	 *
	 * @throws Exception: The re-thrown unexpected Exception
	 */
	public function execute() {

		try {
			if ($this->authenticationRequired) {
				$this->userLoggedInCheck();
			}
			$this->defineBehaviour();
			header("Location: " . $_SERVER["HTTP_REFERER"]);

		} catch (ActionException $e) {
			$e->storeMessageInSession();
			$e->setHeaderToRedirect();

		} catch (Exception $e) {
			echo "Oops... Something broke on our end, sorry!";
			$this->db->close();
			throw $e;
		}
		$this->db->close();
	}

	/**
	 * Makes sure that the user is logged in. If not, a
	 * DangerException is thrown
	 * @throws DangerException: When the user is not logged in
	 */
	protected function userLoggedInCheck() {

		$authError = new DangerException(
			"ACTION_FAIL_AUTH", $_SERVER["HTTP_REFERER"]);

		if (!isset($_SESSION["user_id"])) {
			throw $authError;
		}

		$auth = new Authenticator(Functions::getMysqli());
		$user = $auth->getUserFromId($_SESSION["user_id"]);

		if ($user === null || !$user->isLoggedIn()) {
			throw $authError;
		}
	}
}