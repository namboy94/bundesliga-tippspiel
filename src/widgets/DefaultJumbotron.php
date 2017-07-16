<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 8:03 PM
 */

namespace bundesliga_tippspiel;
use chameleon_widgets\TitleJumboTron;


class DefaultJumbotron extends TitleJumboTron {

	public function __construct(string $title) {
		parent::__construct(
			new DefaultDictionary(),
			$title,
			"resources/grass.jpg");
	}

}