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
use champlates\BootstrapScript;
use champlates\BootstrapStyleSheet;
use champlates\GoogleAnalyticsScript;
use champlates\Header;
use champlates\ReCaptchaScript;
use champlates\Stylesheet;


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
			new Stylesheet("css/custom.css"),
			new Stylesheet("css/champlates.css"),
			new Stylesheet("css/comments.css")
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