<?php

namespace bundesliga_tippspiel;
use chameleon\HtmlElement;
use welwitschi\Authenticator;
use mysqli;

class Page extends HtmlElement {

	protected $db;
	protected $authenticator;
	protected $user;
	protected $isLoggedIn;

	public function __construct(string $title,
								string $navTitle,
								string $jumboTitle) {
		$dictionary = new DefaultDictionary();
		parent::__construct(__DIR__ . "/templates/page.html", $dictionary);

		$this->db = new mysqli(
			"localhost",
			"tippspiel",
			file_get_contents(__DIR__ . "/../../../database_pswd.txt"),
			"bundesliga_tippspiel");
		$this->authenticator = new Authenticator($this->db);

		if (isset($_SESSION["user_id"])) {
			$this->user =
				$this->authenticator->getUserFromId($_SESSION["user_id"]);
		} else {
			$user = null;
		}

		if ($this->user === null) {
			$this->isLoggedIn = false;
		} else {
			$this->isLoggedIn = $this->user->isLoggedIn();
		}

		$header = new DefaultHeader($title);
		$navbar = new DefaultNavbar($navTitle, $this->isLoggedIn);

		$this->addInnerElements(["HEADER" => $header, "NAVBAR" => $navbar]);
	}
}