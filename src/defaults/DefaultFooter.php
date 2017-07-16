<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 7:49 PM
 */

namespace bundesliga_tippspiel;
use chameleon\Footer;
use chameleon\Hyperlink;
use chameleon\NavbarButton;


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

		parent::__construct(
			$dict,
			new Hyperlink("@{FOOTER_TITLE}", "about.php"),
			[$authorButton],
			[$sourceButton]);
	}

}