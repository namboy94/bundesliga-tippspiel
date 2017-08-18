<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 8/18/17
 * Time: 1:15 AM
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
	 * @param Throwable $t: The thrown exception
	 */
	public function onNotSuccessfulTest(Throwable $t) {
		parent::onNotSuccessfulTest($t);
		if (is_file(ApiAction::$inputStream)) {
			unlink(ApiAction::$inputStream);
		}
	}

	/**
	 * Deletes the temporary JSON file
	 */
	public function tearDown() {
		parent::tearDown();
		if (is_file(ApiAction::$inputStream)) {
			unlink(ApiAction::$inputStream);
		}
	}
}