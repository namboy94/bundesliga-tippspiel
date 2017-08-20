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

namespace bundesliga_tippspiel_tests;

use bundesliga_tippspiel_api\AuthorizeApiAction;


/**
 * Class GetUserBetsForMatchdayApiActionTest
 * @package bundesliga_tippspiel_tests
 */
class AuthorizeApiActionTest extends GenericApiTest {

	/**
	 * Tests successfully authenticating
	 */
	public function testSuccessfulAuthorization() {
		$result = $this->executeApiAction(AuthorizeApiAction::class,
			[
				"username" => "A",
				"api_key" => $this->confirmedUserA->generateNewApiKey()
			]
		);
		$this->assertEquals($result["status"], "success");
	}

	/**
	 * Tests authenticating with incorrect credentials
	 */
	public function testUnsuccessfulAuthorization() {
		$result = $this->executeApiAction(AuthorizeApiAction::class,
			["username" => "A", "api_key" => "B"]);
		$this->assertEquals($result["status"], "error");
	}

}