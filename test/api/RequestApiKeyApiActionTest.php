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

namespace bundesliga_tippspiel_tests;

use bundesliga_tippspiel_api\RequestApiKeyApiAction;

/**
 * Class RequestApiKeyApiActionTest
 * Tests the API Action request_api_key
 * @package bundesliga_tippspiel_tests
 */
class RequestApiKeyApiActionTest extends GenericApiTest {

	/**
	 * Tests retrieving an API Key using a correct username and password
	 */
	public function testGettingApiKey() {

		$result = $this->executeApiAction(RequestApiKeyApiAction::class,
			["username" => "A", "password" => "A"]);
		$this->assertEquals($result["status"], "success");
		$this->assertTrue(isset($result["key"]));

	}

	/**
	 * Tests retrieving an API key for a user while using
	 * an incorrect password
	 */
	public function testGettingApiKeyWithWrongPassword() {

		$result = $this->executeApiAction(RequestApiKeyApiAction::class,
			["username" => "A", "password" => "B"]);
		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "credential_check_failed");
		$this->assertFalse(isset($result["key"]));

	}

	/**
	 * Tests retrieving an API key for a user that does not exist
	 */
	public function testGettingApiKeyForNotExistingUser() {

		$result = $this->executeApiAction(RequestApiKeyApiAction::class,
			["username" => "Z", "password" => "A"]);
		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "invalid_user");
		$this->assertFalse(isset($result["key"]));

	}

	/**
	 * Tests retrieving an API key for an unconfirmed user
	 */
	public function testGettingApiKeyForUnconfirmedUser() {

		$result = $this->executeApiAction(RequestApiKeyApiAction::class,
			["username" => "B", "password" => "B"]);
		$this->assertEquals($result["status"], "error");
		$this->assertEquals($result["cause"], "unconfirmed_user");
		$this->assertFalse(isset($result["key"]));

	}

	/**
	 * Checks that all required parameters have to be supplied
	 */
	public function testInvalidJson() {

		foreach ([[], ["username" => "A"], ["password" => "A"]] as $config) {
			$result = $this->executeApiAction(RequestApiKeyApiAction::class,
				$config);
			$this->assertEquals($result["status"], "error");
			$this->assertEquals($result["cause"], "missing_parameter");
			$this->assertFalse(isset($result["key"]));
		}
	}
}