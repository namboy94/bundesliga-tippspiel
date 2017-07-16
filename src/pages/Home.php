<?php

namespace bundesliga_tippspiel;
use chameleon_bootstrap\Row;


/**
 * Class Home
 * The Home Page available when calling index.php
 * @package bundesliga_tippspiel
 */
class Home extends Page {

	/**
	 * Home constructor.
	 */
	public function __construct() {

		$jumboTitle = $this->isUserLoggedIn() ?
			$this->user->username : "@{HOME_JUMBO_TITLE}";

		$content = [new Row(null)];

		parent::__construct(
			"@{HOME_TITLE}",
			$jumboTitle,
			"index.php",
			$content
		);
	}
}
