<?php

namespace bundesliga_tippspiel;


class Home extends Page {

	public function __construct() {

		$jumboTitle = $this->isLoggedIn ?
			$this->user->username : "@{HOME_JUMBO_TITLE}";

		parent::__construct(
			"@{HOME_TITLE}",
			"@{HOME_NAVBAR_TITLE}",
			$jumboTitle
		);
	}

}