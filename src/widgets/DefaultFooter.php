<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 7:49 PM
 */

namespace bundesliga_tippspiel;
use chameleon_widgets\Footer;
use chameleon_widgets\Hyperlink;
use chameleon_widgets\NavbarButton;


class DefaultFooter extends Footer {

	public function __construct(string $pageName) {

		$dict = new DefaultDictionary();
		$authorSelected = $pageName === "contact.php";

		$authorButton = new NavbarButton(
			$dict,
			new Hyperlink("© Hermann Krumrey 2017", "contact.php"),
			$authorSelected
		);

		$version = file_get_contents(__DIR__ . "/../../version");
		$gitlab = "https://gitlab.namibsun.net/namboy94/bundesliga-tippspiel";
		$sourceButton = new NavbarButton(
			$dict, new Hyperlink($version, $gitlab), false
		);

		parent::__construct(
			$dict,
			new Hyperlink("@{FOOTER_TITLE}", "about.php"),
			[$authorButton],
			[$sourceButton]);
	}

}