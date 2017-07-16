<?php

namespace bundesliga_tippspiel;
use chameleon\HtmlElement;
use chameleon_widgets\Div;
use welwitschi\Authenticator;
use mysqli;

class Page extends HtmlElement {

	protected $db;
	protected $authenticator;
	protected $user;
	protected $isLoggedIn;

	public function __construct(string $title,
								string $navTitle,
								string $jumboTitle,
								string $pageFile,
								array $content) {
		$dictionary = new DefaultDictionary();
		parent::__construct(__DIR__ . "/templates/page.html", $dictionary);

		$this->db = new mysqli(
			"localhost",
			"tippspiel",
			file_get_contents(__DIR__ . "/../../DB_PASS.secret"),
			"tippspiel_bundesliga");
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

		if ($this->isLoggedIn) {
			$body = [
				new Div($content, ["col-sm-9", "main-content"]),
				new Div([new CommentBar($this->user)],
					["col-sm-3", "comments"])];
		} else {
			$body = [new Div($content, ["col-sm-12", "main-content"])];
		}

		$header = new DefaultHeader($title);
		$navbar = new DefaultNavbar($navTitle, $this->isLoggedIn);
		$jumbotron = new DefaultJumbotron($jumboTitle);
		$footer = new DefaultFooter($pageFile);

		$this->addInnerElements([
			"HEADER" => $header,
			"NAVBAR" => $navbar,
			"FOOTER" => $footer,
			"JUMBOTRON" => $jumbotron,
			"BODY" => $body
		]);
	}
}