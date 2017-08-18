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

namespace bundesliga_tippspiel_actions;
use bundesliga_tippspiel\DefaultDictionary;
use bundesliga_tippspiel\Functions;
use chameleon\ForgottenPasswordForm;
use chameleon\FormReCaptcha;
use welwitschi\Authenticator;

/**
 * Class PasswordResetAction
 * Enables the user to reset their password
 * @package bundesliga_tippspiel_actions
 */
class PasswordResetAction extends Action {

	/**
	 * PasswordResetAction constructor.
	 * @param bool $authenticationRequired: Set to false since resetting the
	 *                                      password does not require login
	 */
	public function __construct($authenticationRequired = false) {
		parent::__construct($authenticationRequired);
	}

	/**
	 * Defines the behaviour of the Action
	 * @return void
	 * @throws ActionException: The message information
	 */
	protected function defineBehaviour() {

		$email = $_POST[ForgottenPasswordForm::$email];
		$recaptcha = $_POST[FormReCaptcha::$recaptchaPostKey];


		if ($_SERVER["SERVER_NAME"] !== "localhost"
			&& !Functions::verifyCaptcha($recaptcha)) {
			// We only check for valid captchas on the production server,
			// not on the development machine, since the ReCaptcha settings
			// are not configured for `localhost`

			// @codeCoverageIgnoreStart
			throw new DangerException(
				"RESET_PASSWORD_ERROR_RECAPTCHA", "../forgot.php");
			// @codeCoverageIgnoreEnd

		} else {

			$dict = new DefaultDictionary();
			$auth = new Authenticator($this->db);
			$user = $auth->getUserFromEmailAddress($email);

			if ($user !== null) {

				$password = $user->resetPassword();

				// Send Email with new temporary password
				mail($email,
					$dict->translate("@{PASSWORD_RESET_EMAIL_TITLE}",
						Functions::getLanguage()),
					$dict->translate("@{PASSWORD_RESET_EMAIL_BODY_START}\n\n" .
						$password . "\n\n@{PASSWORD_RESET_EMAIL_BODY_END}",
						Functions::getLanguage()));
			}

			// Even if no user with that email address was found, we still
			// let the user think a reset email was sent to make it harder to
			// figure out which email addresses have been used by our users.
			throw new SuccessException("RESET_PASSWORD_SUCCESS",
				"../index.php");
		}
	}
}