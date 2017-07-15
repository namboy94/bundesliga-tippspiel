<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:59 AM
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon_widgets\Hyperlink;
use chameleon_widgets\Navbar;
use chameleon_widgets\NavbarButton;
use chameleon_widgets\NavbarLogo;


class DefaultNavbar extends Navbar {

	public function __construct(string $pageName, bool $loggedIn) {

		$dict = new DefaultDictionary();

		$homeSelected = $pageName === "Home";

		$homeButton = new NavbarButton(
			$dict, new Hyperlink("@{HOME_TITLE}", "index.php"), $homeSelected);

		$leftElements = [$homeButton];
		$rightElements = [];

		parent::__construct(
			$dict,
			new Hyperlink("@{NAVBAR_TITLE}", "index.php"),
			$leftElements,
			$rightElements,
			null
		);
	}
}