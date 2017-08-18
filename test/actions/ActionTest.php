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
use bundesliga_tippspiel\Functions;
use bundesliga_tippspiel_actions\Action;
use bundesliga_tippspiel_actions\InfoException;
use PHPUnit\Framework\TestCase;
use Exception;


/**
 * Class ActionTest
 * Tests the parts of the Action class not already tested using the various
 * other Actions
 * @package bundesliga_tippspiel_tests
 */
class ActionTest extends TestCase {

	/**
	 * Tests if an exception is correctly handled by the execute() method
	 * @SuppressWarnings checkUnusedVariables
	 */
	public function testExceptionHandling() {

		if (!isset($_SESSION)) {
			session_start();
		}
		$_SERVER["SERVER_NAME"] = "localhost";
		$_SERVER["HTTP_REFERER"] = "localhost";
		Functions::$dbdatabase = "tippspiel_bundesliga_test";
		Functions::$dbusername = "phpunit";

		ob_start();
		$action = new Derived();

		try {
			$action->execute();
			$this->fail();
		} catch (Exception $e) {
			$content = ob_get_contents();
			$this->assertEquals($content,
				"Oops... Something broke on our end, sorry!");
			$this->assertEquals($e->getMessage(), "Test");
		}

		ob_end_clean();
	}

	/**
	 * Tests the Info Exception, since it's never used by any current actions
	 */
	public function testInfoException() {
		new InfoException("A", "A");
		$this->assertTrue(true);
	}

}

/**
 * Class Derived
 * Child class of an Action that implements a behaviour that always
 * leads to an exception
 * @package bundesliga_tippspiel_tests
 * @SuppressWarnings oneClassPerFile
 */
class Derived extends Action {

	/**
	 * Derived constructor.
	 * @param bool $authenticationRequired: Set to false
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws Exception
	 */
	protected function defineBehaviour() {
		throw new Exception("Test");
	}
}