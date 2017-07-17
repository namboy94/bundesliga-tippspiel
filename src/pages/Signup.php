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
class Signup extends Page {

	/**
	 * Signup constructor.
	 */
	public function __construct() {

		$register = new SignupForm(
			$this->dictionary,
			"@{SIGNUP_REGISTER_FORM_TITLE}",
			"actions/signup.php",
			"6LegcBQUAAAAAOFRbqARHxlbnpfIM3Po0ijzIA1M"
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

		$box = new Container([new Row([
			$registerCol, $divider, $loginCol
		])]);

		parent::__construct(
			"@{SIGNUP_TITLE}",
			"@{SIGNUP_JUMBO_TITLE}",
			"signup.php",
			[$box]
		);

		$header = new DefaultHeader("@{SIGNUP_TITLE}", true);
		$this->addInnerTemplate("HEADER", $header);

	}
}