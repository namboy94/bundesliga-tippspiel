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
use chameleon\BootstrapScript;
use chameleon\BootstrapStyleSheet;
use chameleon\GoogleAnalyticsScript;
use chameleon\Header;
use chameleon\ReCaptchaScript;
use chameleon\Stylesheet;


/**
 * Class DefaultHeader
 * The Header displayed in the <head> section of pretty much every page
 * @package bundesliga_tippspiel
 */
class DefaultHeader extends Header {

	/**
	 * DefaultHeader constructor.
	 * @param string $title: The title of the page
	 * @param bool $useRecaptcha: Can be set to true to enable Recaptcha
	 */
	public function __construct(string $title, bool $useRecaptcha = false) {

		$scripts = [
			new BootstrapScript(),
			new GoogleAnalyticsScript("UA-77243880-6"),
			new BootstrapStyleSheet()
		];

		$styleSheets = [
			new BootstrapStyleSheet(),
			new Stylesheet("css/custom.css")
		];

		if ($useRecaptcha) {
			array_push($scripts, new ReCaptchaScript());
		}

		parent::__construct(
			new DefaultDictionary(),
			$title,
			"resources/images/favicon.png",
			$scripts,
			$styleSheets
		);
	}
}