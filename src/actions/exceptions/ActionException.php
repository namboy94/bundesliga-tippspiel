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
 * Class ActionException
 * Exception class used to signal an Event that went wrong
 * @package bundesliga_tippspiel_actions
 */
class ActionException extends Exception {

	/**
	 * @var string: The message identifier for this exception
	 */
	private $messageIdentifier;

	/**
	 * @var string: The message type
	 */
	private $messageType;

	/**
	 * @var string: The location to redirect to
	 */
	private $redirect;

	/**
	 * ActionException constructor.
	 * @param string $messageIdentifier: The error message identifier
	 * @param string $messageType: The type of error message
	 * @param string $redirect: The URL to redirect to
	 */
	public function __construct(
		string $messageIdentifier, string $messageType, string $redirect) {
		$this->messageIdentifier = $messageIdentifier;
		$this->redirect = $redirect;
		parent::__construct();
	}

	/**
	 * Stores the message in the session variable
	 */
	public function storeMessageInSession() {
		$_SESSION["message"] = [
			"type" => $this->messageType,
			"title" => "@{" . $this->messageIdentifier . "_TITLE}",
			"body" => "@{" . $this->messageIdentifier . "_BODY}"
		];
	}

	/**
	 * Sets the redirect header to the redirect location
	 */
	public function setHeaderToRedirect() {
		header("Location: " . $this->redirect);
	}

}