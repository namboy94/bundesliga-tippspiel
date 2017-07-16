<?php

namespace bundesliga_tippspiel;


use chameleon_widgets\Div;

class Home extends Page {

	public function __construct() {

		$jumboTitle = $this->isLoggedIn ?
			$this->user->username : "@{HOME_JUMBO_TITLE}";

		parent::__construct(
			"@{HOME_TITLE}",
			"@{HOME_NAVBAR_TITLE}",
			$jumboTitle,
			"index.php",
			$content
		);

		$box = new Div("a", ["row"]);
		$content = new Div("a", ["col-sm-12 main-content"]);



		$content = [];


	}
}
