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
use chameleon\ForgottenPasswordForm;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;


/**
 * Class Forgot
 * The Forgotten Password Page
 * @package bundesliga_tippspiel
 */
class Forgot extends Page {

	/**
	 * Forgot constructor.
	 */
	public function __construct() {

		$form = new ForgottenPasswordForm(
			$this->dictionary,
			"@{FORGOT_FORM_TITLE}",
			"actions/password_reset.php",
			Functions::getRecaptchaSiteKey()
		);

		$box = new Container([new Row([$form])]);

		parent::__construct(
			"@{FORGOT_TITLE}",
			"{FORGOT_JUMBO_TITLE}",
			"forgot.php",
			[$box]
		);

		$header = new DefaultHeader("@{FORGOT_TITLE}", true);
		$this->addInnerTemplate("HEADER", $header);
	}

}