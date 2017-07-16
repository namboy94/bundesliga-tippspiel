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
use chameleon\Hyperlink;
use chameleon\Navbar;
use chameleon\NavbarButton;
use chameleon\NavbarLogo;


/**
 * Class DefaultNavbar
 * The Default Navbar of the website. Offers different Elements
 * when the user is logged in Vs if not. The current page will
 * also be selected as long as that page has a button in the bar.
 * @package bundesliga_tippspiel
 */
class DefaultNavbar extends Navbar {

	/**
	 * DefaultNavbar constructor.
	 * @param string $pageFile: The Filename of the page displaying the Navbar
	 * @param bool $loggedIn: Indicates if the user is logged in or not
	 */
	public function __construct(string $pageFile, bool $loggedIn) {

		$dict = new DefaultDictionary();

		$homeButton = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_HOME_TITLE}", "index.php"),
			$pageFile === "index.php"
		);

		$loginButton = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_LOGIN_TITLE}", "signup.php"),
			$pageFile === "signup.php"
		);

		$logoutButton = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_LOGOUT_TITLE}", "actions/logout.php"),
			false
		);

		$bets = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_BETS_TITLE}", "bets.php"),
			$pageFile === "bets.php"
		);

		$leaderboard = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_LEARBOARD_TITLE}", "leaderboard.php"),
			$pageFile === "leaderboard.php"
		);

		$profile = new NavbarButton(
			$dict,
			new Hyperlink("@{NAVBAR_PROFILE_TITLE}", "profile.php"),
			$pageFile === "profile.php"
		);

		if ($loggedIn) {
			$leftElements = [$homeButton, $bets, $leaderboard, $profile];
			$rightElements = [$logoutButton];
		} else {
			$leftElements = [$homeButton, $loginButton];
			$rightElements = [];
		}

		parent::__construct(
			$dict,
			new Hyperlink("@{NAVBAR_TITLE}", "index.php"),
			$leftElements,
			$rightElements,
			new NavbarLogo("resources/images/favicon.png", "index.php")
		);
	}
}