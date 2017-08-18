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
use mysqli;


/**
 * Class Functions
 * Class that contains various helpful functions
 * @package bundesliga_tippspiel
 */
class Functions {

	/**
	 * @var string: The database to use
	 */
	public static $dbdatabase = "tippspiel_bundesliga";

	/**
	 * @var string: The database user to use
	 */
	public static $dbusername = "tippspiel";

	/**
	 * @return mysqli: The MySQL Database connection
	 */
	public static function getMysqli(): mysqli {
		return new mysqli(
			"localhost",
			self::$dbusername,
			rtrim(file_get_contents(__DIR__ . "/../../DB_PASS.secret")),
			self::$dbdatabase
		);
	}

	/**
	 * Initializes a session and sets the lifetime of the cookies
	 */
	public static function initializeSession() {
		if (!isset($_SESSION)) {
			session_start();
			session_set_cookie_params(
				86400,
				null,
				$_SERVER["SERVER_NAME"],
				true,
				true);
		}
	}

	/**
	 * Verifies a captcha
	 * @param $captchaContent string: The captcha POST key
	 * @return bool: true if verified, else false
	 */
	public static function verifyCaptcha(string $captchaContent) {
		$secretKey = file_get_contents(
			__DIR__ . "/../../RECAPTCHA_SITE_KEY.secret");

		$url = 'https://www.google.com/recaptcha/api/siteverify';
		$params = 'secret=' . $secretKey .
			'&response=' . $captchaContent .
			'&remoteip=' . $_SERVER['REMOTE_ADDR'];

		$curl = curl_init($url);
		curl_setopt($curl, CURLOPT_POST, 1);
		curl_setopt($curl, CURLOPT_POSTFIELDS, $params);
		curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
		curl_setopt($curl, CURLOPT_HEADER, 0);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

		$response = curl_exec($curl);
		$data = json_decode($response);
		return (bool)$data->success;
	}

	/**
	 * @return string: The site's recaptcha site key
	 */
	public static function getRecaptchaSiteKey() : string {
		return "6LefYikUAAAAAMrA5hQAtIzAqyWnFOSnBjrVSUyr";
	}

	/**
	 * @return string: The currently active language
	 */
	public static function getLanguage() : string {
		return "de";
	}
}