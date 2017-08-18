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

namespace bundesliga_tippspiel_api;

/**
 * Class RequestApiKeyApiAction
 * Class that handles requesting a new API key for a user
 * @package bundesliga_tippspiel_api
 */
class RequestApiKeyApiAction extends ApiAction {

	/**
	 * RequestApiKeyApiAction constructor.
	 * Overrides the constructor to make this API action
	 * not require authentication
	 * @param bool $authenticationRequired: false
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: To signify error cases
	 */
	protected function defineBehaviour(): array {

		$username = $this->inputData["username"];
		$password = $this->inputData["password"];
		$user = $this->authenticator->getUserFromUsername($username);

		if ($user === null) {
			throw new ApiException("invalid_user");
		} elseif (!$user->doesPasswordMatch($password)) {
			throw new ApiException("credential_check_failed");
		} else {
			$apiKey = $user->generateNewApiKey();
			if ($apiKey === null) {
				throw new ApiException("unconfirmed_user");
			} else {
				return ["key" => $apiKey];
			}
		}
	}

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public function defineRequiredParameters(): array {
		return ["username", "password"];
	}
}