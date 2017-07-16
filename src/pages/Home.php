<?php

namespace bundesliga_tippspiel;
use chameleon\HtmlTemplate;
use chameleon\LoginForm;
use chameleon_bootstrap\Col;
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


		$summary = new HtmlTemplate(__DIR__ . "/templates/home_summary.html",
			$this->dictionary);

		$login = new LoginForm($this->dictionary,
			"@{HOME_LOGIN_TITLE}", "actions/login.php");

		$summaryCol = new Col([$summary], 8, ["text-center"]);
		$loginCol = new Col([$login], 4, ["text-center"]);

		$content = [
			new Row([$summaryCol, $loginCol]),
			new DefaultFooter("index.php")
		];

		parent::__construct(
			"@{HOME_TITLE}",
			$jumboTitle,
			"index.php",
			$content
		);
	}
}
