<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 8:03 PM
 */

namespace bundesliga_tippspiel;
use chameleon\TitleJumboTron;


/**
 * Class DefaultJumbotron
 * The Default Jumbotron to display on the top of the page
 * @package bundesliga_tippspiel
 */
class DefaultJumbotron extends TitleJumboTron {

	/**
	 * DefaultJumbotron constructor.
	 * @param string $title: The title of the Jumbotron
	 */
	public function __construct(string $title) {
		parent::__construct(
			new DefaultDictionary(),
			$title,
			"resources/images/grass.jpg");
		$this->changeTemplate(__DIR__ . "/templates/default_jumbotron.html");
	}
}