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
use Exception;

/**
 * Class ApiException
 * A specialized API Exception that can be used to communicate an error state
 * @package bundesliga_tippspiel_api
 */
class ApiException extends Exception {

	/**
	 * @var string: The description of the error
	 */
	private $errorDescription;

	/**
	 * ApiException constructor.
	 * @param string $errorDescription: The error description
	 */
	public function __construct(string $errorDescription) {
		$this->errorDescription = $errorDescription;
		parent::__construct();
	}

	/**
	 * Turns the exception into a JSON response array
	 * @return array: The JSON response array
	 */
	public function toArray() : array {
		return ["status" => "error", "cause" => $this->errorDescription];
	}

}