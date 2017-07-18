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
use chameleon\Html;
use chameleon\HtmlTemplate;
use chameleon\LoginForm;
use chameleon_bootstrap\Col;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;


/**
 * Class Home
 * The Home Page available when calling index.php
 * @package bundesliga_tippspiel
 */
class HomePage extends Page {

	/**
	 * Home constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{HOME_TITLE}",
			"",
			"index.php"
		);
		$jumboTitle = $this->isUserLoggedIn() ?
			$this->user->username : "@{HOME_JUMBO_TITLE}";
		$jumbotron = new DefaultJumbotron($jumboTitle);
		$this->addInnerTemplate("JUMBOTRON", $jumbotron);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {
		$summary = new HtmlTemplate(__DIR__ . "/templates/home_summary.html",
			$this->dictionary);

		$login = new LoginForm($this->dictionary,
			"@{HOME_LOGIN_TITLE}", "actions/login.php");
		$registerMessage = new Html("@{HOME_REGISTER_MESSAGE}");

		$summaryCol = new Col([$summary], 8, ["text-center"]);
		$loginCol = new Col([$login, $registerMessage], 4, ["text-center"]);

		return [new Row([$summaryCol, $loginCol])];
	}
}
