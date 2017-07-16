<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:59 AM
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