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
