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
use chameleon\Footer;
use chameleon\Hyperlink;
use chameleon\NavbarButton;
use chameleon\NavbarLogo;


/**
 * Class DefaultFooter
 * The default footer at the bottom of the page
 * @package bundesliga_tippspiel
 */
class DefaultFooter extends Footer {

	/**
	 * DefaultFooter constructor.
	 * @param string $pageFile: The page's file name
	 */
	public function __construct(string $pageFile) {

		$dict = new DefaultDictionary();

		$authorButton = new NavbarButton(
			$dict,
			new Hyperlink("© Hermann Krumrey 2017", "contact.php"),
			$pageFile === "contact.php"
		);

		$version = file_get_contents(__DIR__ . "/../../version");
		$gitlab = "https://gitlab.namibsun.net/namboy94/bundesliga-tippspiel";
		$sourceButton = new NavbarButton(
			$dict, new Hyperlink($version, $gitlab), false
		);

		$champlatesLogo = new NavbarLogo(
			"resources/images/logos/champlates.png",
			"https://gitlab.namibsun.net/namboy94/champlates"
		);
		$cheetahBetsLogo = new NavbarLogo(
			"resources/images/logos/cheetah-bets.png",
			"https://gitlab.namibsun.net/namboy94/cheetah-bets"
		);
		$welwitschiAuthLogo = new NavbarLogo(
			"resources/images/logos/welwitschi-auth.png",
			"https://gitlab.namibsun.net/namboy94/welwitschi-auth"
		);

		parent::__construct(
			$dict,
			new Hyperlink("@{FOOTER_TITLE}", "about.php"),
			[$authorButton],
			[
				$champlatesLogo,
				$cheetahBetsLogo,
				$welwitschiAuthLogo,
				$sourceButton
			],
			true
		);
	}

}