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
use champlates\ChangePasswordForm;
use champlates\ChangeUsernameForm;
use champlates\ChangeEmailForm;
use champlates_bootstrap\Col;
use champlates_bootstrap\Row;


/**
 * Class Profile
 * A Profile page which allows users to manage their accounts
 * @package bundesliga_tippspiel
 */
class ProfilePage extends Page {

	/**
	 * Profile constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{PROFILE_TITLE}",
			"@{PROFILE_JUMBO_TITLE}",
			"profile.php",
			true
		);
		$jumbotron = new DefaultJumbotron(
			$this->user->username . "<br>" . $this->user->email
		);
		$this->addInnerTemplate("JUMBOTRON", $jumbotron);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {

		$passwordChange = new ChangePasswordForm(
			$this->dictionary,
			"@{PROFILE_CHANGE_PASSWORD_FORM_TITLE}",
			"actions/change_password.php"
		);

		$usernameChange = new ChangeUsernameForm(
			$this->dictionary,
			"@{PROFILE_CHANGE_USERNAME_FORM_TITLE}",
			"actions/change_username.php"
		);

		$emailChange = new ChangeEmailForm(
			$this->dictionary,
			"@{PROFILE_CHANGE_EMAIL_FORM_TITLE}",
			"actions/change_email.php"
		);

		$content = [
			new Col([], 1),
			new Col([$passwordChange], 4),
			new Col([], 2),
			new Col([$usernameChange, $emailChange], 4),
			new Col([], 1)
		];

		return [new Row($content)];
	}
}