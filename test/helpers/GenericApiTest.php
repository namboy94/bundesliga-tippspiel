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

use bundesliga_tippspiel_api\ApiAction;
use Throwable;


/**
 * Class GenericApiTest
 * Provides helper methods and states for an API test
 * @package bundesliga_tippspiel_tests
 */
abstract class GenericApiTest extends TestClass {

	/**
	 * Sets the input file for the API action
	 */
	public function setUp() {
		parent::setUp();
		ApiAction::$inputStream = __DIR__ . "tempfile";
	}

	/**
	 * Executes an API Action and captures the result
	 * @param $apiAction: The API action to test
	 * @param array $inputJson: The input JSON data
	 * @return array: The result JSON array
	 * @SuppressWarnings docBlocks
	 * @SuppressWarnings checkProhibitedFunctions
	 */
	protected function executeApiAction($apiAction, array $inputJson) : array {

		file_put_contents(ApiAction::$inputStream, json_encode($inputJson));
		ob_start();
		/** @noinspection PhpUndefinedMethodInspection */
		(new $apiAction())->execute();
		$response = ob_get_contents();
		ob_end_clean();
		unlink(ApiAction::$inputStream);

		return json_decode($response, true);
	}

	/**
	 * Deletes the temporary file if the test was not successful
	 * @param Throwable $throwable: The thrown exception
	 * @SuppressWarnings checkProhibitedFunctions
	 */
	public function onNotSuccessfulTest(Throwable $throwable) {
		parent::onNotSuccessfulTest($throwable);
		if (is_file(ApiAction::$inputStream)) {
			unlink(ApiAction::$inputStream);
		}
	}

	/**
	 * Deletes the temporary JSON file
	 * @SuppressWarnings checkProhibitedFunctions
	 */
	public function tearDown() {
		parent::tearDown();
		if (is_file(ApiAction::$inputStream)) {
			unlink(ApiAction::$inputStream);
		}
	}
}