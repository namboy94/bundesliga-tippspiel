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
use cheetah\Goal;

/**
 * API endpoint for retriving all goals for a match
 * @package bundesliga_tippspiel_api
 */
class GetGoalDataForMatchApiAction extends ApiAction {

	/**
	 * Defines the behaviour of the API Action
	 * @return array: The returned JSON array data
	 * @throws ApiException: If the API Action could not be completed
	 */
	protected function defineBehaviour(): array {
		$db = Functions::getMysqli();
		$goals = Goal::getFromMatchId($db, $this->inputData["match_id"]);
		$db->close();

		$data = [];

		foreach ($goals as $goal) {
			/** @noinspection PhpUndefinedMethodInspection */
			array_push($data, $goal->toJsonArray());
		}

		return ["data" => $data];
	}

	/**
	 * Defines the required JSON parameters in the API query
	 * @return array: A list of required JSON parameters
	 */
	public function defineRequiredParameters(): array {
		return ["match_id"];
	}
}