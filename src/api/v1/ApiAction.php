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

namespace bundesliga_tippspiel_api;
use bundesliga_tippspiel\Functions;
use ErrorException;
use mysqli;
use welwitschi\Authenticator;

/**
 * Class ApiAction
 * An abstract template for an API action
 * @package bundesliga_tippspiel_api
 */
abstract class ApiAction {

	/**
	 * @var bool: Defines if the API Action requires authentication or not
	 */
	protected $authenticationRequired;

	/**
	 * @var array: The POSTed JSON data
	 */
	protected $inputData;

	/**
	 * @var mysqli: The MySQL database connection
	 */
	protected $db;

	/**
	 * @var Authenticator: The authenticator for user-related operations
	 */
	protected $authenticator;

	/**
	 * @var string: The input stream location for the POST data
	 */
	public static $inputStream = "php://input";

	/**
	 * ApiAction constructor.
	 * @param bool $authenticationRequired: See class variable description
	 */
	public function __construct(bool $authenticationRequired = true) {
		$this->authenticationRequired = $authenticationRequired;
		$this->db = Functions::getMysqli();
		$this->authenticator = new Authenticator($this->db);
		$this->inputData =
			json_decode(file_get_contents(self::$inputStream), true);
	}

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: If the API Action could not be completed
	 */
	protected abstract function defineBehaviour() : array;

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public abstract function defineRequiredParameters() : array;

	/**
	 * Executes the API action, checks for exceptions, and if everything
	 * was successful, sends the appropriate JSON response
	 * @SuppressWarnings docBlocks
	 */
	public function execute() {

		header('Content-Type: application/json');

		set_error_handler(function($errno, $errstr, $errfile, $errline) {
			throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
		});

		// Check for missing parameters
		foreach ($this->defineRequiredParameters() as $param) {
			// username and api_key are implicitly checked by the auth check
			if (!isset($this->inputData[$param])) {
				echo json_encode(
					["status" => "error", "cause" => "missing_parameter"]
				);
				return;
			}
		}

		if ($this->authenticationRequired && !$this->isAuthenticated()) {
			$retval = ["status" => "error", "cause" => "unauthorized"];
		} else {
			try {
				$retval = $this->defineBehaviour();
				if (!isset($retval["status"])) {
					$retval["status"] = "success";
				}
			} catch (ApiException $e) {
				$retval = $e->toArray();
			} catch (ErrorException $e) {
				$retval = ["status" => "error", "cause" => "exception"];
			}
		}
		echo json_encode($retval);
		$this->db->close();
	}

	/**
	 * Checks if the API request was authenticated correctly
	 * @return bool: The result of the check
	 */
	public function isAuthenticated() : bool {

		if (!isset($this->inputData["username"])
			&& !isset($this->inputData["api_key"])) {
			return false;
		}

		$username = $this->inputData["username"];
		$apiKey = $this->inputData["api_key"];

		$user = $this->authenticator->getUserFromUsername($username);

		if ($user === null) {
			return false;
		} else {
			return $user->verifyApiKey($apiKey);
		}
	}
}