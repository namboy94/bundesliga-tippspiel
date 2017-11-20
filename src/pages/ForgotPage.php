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
use champlates\ForgottenPasswordForm;
use champlates_bootstrap\Col;
use champlates_bootstrap\Container;
use champlates_bootstrap\Row;


/**
 * Class Forgot
 * The Forgotten Password Page
 * @package bundesliga_tippspiel
 */
class ForgotPage extends Page {

	/**
	 * Forgot constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{FORGOT_TITLE}",
			"@{FORGOT_JUMBO_TITLE}",
			"forgot.php"
		);

		// Enable Recaptcha
		$header = new DefaultHeader("@{FORGOT_TITLE}", true);
		$this->addInnerTemplate("HEADER", $header);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {
		$form = new ForgottenPasswordForm(
			$this->dictionary,
			"@{FORGOT_FORM_TITLE}",
			"actions/password_reset.php",
			Functions::getRecaptchaSiteKey()
		);
		$wrapper = new Col([$form], 6);
		$div = new Col([], 3);
		return [new Row([$div, $wrapper, $div])];
	}
}