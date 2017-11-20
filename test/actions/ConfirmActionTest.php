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
use bundesliga_tippspiel_actions\ConfirmAction;


/**
 * Class CommentActionTest
 * Tests the CommentAction class
 */
class ConfirmActionTest extends TestClass {

	/**
	 * Tests confirming a user
	 */
	public function testSuccessfullyConfirmingUser() {
		$_GET["id"] = $this->unConfirmedUserB->id;
		$_GET["token"] = $this->unConfirmedUserB->confirmationToken;

		(new ConfirmAction())->execute();
		$this->assertStatus("success");
		$this->assertMessageId("CONFIRM_SUCCESS");

		$this->unConfirmedUserB = self::$authenticator->getUserFromId(
			$this->unConfirmedUserB->id);
		$this->assertTrue($this->unConfirmedUserB->confirmed);
	}

	/**
	 * Tests if missing parameters are detected
	 */
	public function testMissingParameters() {

		unset($_GET["id"]);
		unset($_GET["token"]);

		(new ConfirmAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("CONFIRM_FAILED_NO_INPUT");

		$_GET["id"] = $this->unConfirmedUserB->id;
		(new ConfirmAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("CONFIRM_FAILED_NO_INPUT");

		unset($_GET["id"]);
		$_GET["token"] = $this->unConfirmedUserB->confirmationToken;
		(new ConfirmAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("CONFIRM_FAILED_NO_INPUT");

		$this->unConfirmedUserB = self::$authenticator->getUserFromId(
			$this->unConfirmedUserB->id);
		$this->assertFalse($this->unConfirmedUserB->confirmed);

	}

	/**
	 * Tests an unsuccessful confirmation
	 */
	public function testUnsuccessfulConfirmation() {

		$_GET["id"] = $this->unConfirmedUserB->id;
		$_GET["token"] = $this->unConfirmedUserB->confirmationToken . "a";

		(new ConfirmAction())->execute();
		$this->assertStatus("danger");
		$this->assertMessageId("CONFIRM_FAIL");

		$this->unConfirmedUserB = self::$authenticator->getUserFromId(
			$this->unConfirmedUserB->id);
		$this->assertFalse($this->unConfirmedUserB->confirmed);

	}

}