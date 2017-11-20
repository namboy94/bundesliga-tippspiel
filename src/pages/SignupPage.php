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

namespace bundesliga_tippspiel;
use chameleon\Html;
use chameleon\LoginForm;
use chameleon\SignupForm;
use chameleon_bootstrap\Col;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;


/**
 * Class Signup
 * The Signup page which enables a user to log in or register
 * @package bundesliga_tippspiel
 */
class SignupPage extends Page {

	/**
	 * Signup constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{SIGNUP_TITLE}",
			"@{SIGNUP_JUMBO_TITLE}",
			"signup.php"
		);

		$header = new DefaultHeader("@{SIGNUP_TITLE}", true);
		$this->addInnerTemplate("HEADER", $header);

	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {
		$register = new SignupForm(
			$this->dictionary,
			"@{SIGNUP_REGISTER_FORM_TITLE}",
			"actions/signup.php",
			Functions::getRecaptchaSiteKey(),
			10
		);

		$login = new LoginForm(
			$this->dictionary,
			"@{SIGNUP_LOGIN_FORM_TITLE}",
			"actions/login.php"
		);
		$forgotPassword = new Html("@{SIGNUP_FORGOT_PASSWORD_MESSAGE}");

		$registerCol = new Col([$register], 5);
		$loginCol = new Col([$login, $forgotPassword], 5);
		$divider = new Col([], 2);

		$box = new Row([
			$registerCol, $divider, $loginCol
		]);

		return [$box];
	}
}