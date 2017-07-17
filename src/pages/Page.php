<?php
/**
 * Copyright Hermann Krumrey <hermann@krumreyh.com> 2017
 *
 * This file is part of bundesliga_tippspiel.
 *
 * bundesliga_tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga_tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga_tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\DismissableMessage;
use chameleon\HtmlTemplate;
use chameleon_bootstrap\Col;
use cheetah\SchemaCreator;
use welwitschi\Authenticator;
use welwitschi\User;
use mysqli;


/**
 * Class Page
 * A template for all other pages in this project
 * @package bundesliga_tippspiel
 */
abstract class Page extends HtmlTemplate {

	/**
	 * @var mysqli: The Database connection
	 */
	protected $db;

	/**
	 * @var Dictionary: The dictionary used for translations
	 */
	protected $dictionary;

	/**
	 * @var Authenticator: The User Authenticator
	 */
	protected $authenticator;

	/**
	 * @var null|User: The User currently viewing this page. Users that are
	 *                 not logged in are null Users.
	 */
	protected $user;

	/**
	 * Page constructor.
	 * @param string $title : The title of the page (in the header)
	 * @param string $jumboTitle : The title on the page's Jumbotron
	 * @param string $pageFile : The page's file name
	 */
	public function __construct(string $title,
								string $jumboTitle,
								string $pageFile) {
		$this->dictionary = new DefaultDictionary();
		parent::__construct(
			__DIR__ . "/templates/page.html", $this->dictionary);

		// Initialize Authenticator and Database Connections
		$this->db = Functions::getMysqli();
		new SchemaCreator($this->db);
		$this->authenticator = new Authenticator($this->db);
		$this->user = $this->_getUser();

		$header = new DefaultHeader($title);
		$navbar = new DefaultNavbar($pageFile, $this->isUserLoggedIn());
		$jumbotron = new DefaultJumbotron($jumboTitle);
		$footer = new DefaultFooter($pageFile);

		$colSize = $this->isUserLoggedIn() ? 9 : 12;

		$content = $this->setContent();
		array_push($content, $footer);
		$wrapper = new Col($content, $colSize, ["main-content"]);

		$this->addInnerTemplates([
			"HEADER" => $header,
			"NAVBAR" => $navbar,
			"MESSAGE" => $this->_checkForDismissableMessage(),
			"JUMBOTRON" => $jumbotron,
			"BODY" => $wrapper
		]);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected abstract function setContent() : array;

	/**
	 * Checks if the user is logged in.
	 * @return bool: true if the user is logged in, false otherwise
	 */
	protected function isUserLoggedIn() : bool {
		return ($this->user === null) ? false : $this->user->isLoggedIn();
	}

	/**
	 * Retrieves the current user, provided there is a User to retrieve
	 * @return null|User: The User of this page or null.
	 */
	protected function _getUser() : ? User {
		if (isset($_SESSION["user_id"])) {
			return $this->authenticator->getUserFromId($_SESSION["user_id"]);
		} else {
			return null;
		}
	}

	/**
	 * Checks the $_SESSION variable for dismissable message information
	 * @return DismissableMessage|null: The Dismissable Message or null
	 */
	private function _checkForDismissableMessage() : ? DismissableMessage {

		if (isset($_SESSION["message"])) {

			$message = $_SESSION["message"];
			unset($_SESSION["message"]);
			return new DismissableMessage(
				$this->dictionary,
				$message["type"],
				$message["title"],
				$message["body"]
			);

		} else {
			return null;
		}
	}
}