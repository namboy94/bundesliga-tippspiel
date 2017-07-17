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
use chameleon_bootstrap\Col;
use chameleon\HtmlTemplate;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;


/**
 * Class Contact
 * The Contact Page
 * @package bundesliga_tippspiel
 */
class Contact extends Page {

	/**
	 * Contact constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{CONTACT_TITLE}",
			"@{CONTACT_JUMBO_TITLE}",
			"contact.php");
	}

	/**
	 * @return array: The content of this page
	 */
	protected function setContent(): array {

		$dividerOne = new Col([], 1);
		$dividerTwo = new Col([], 2);
		$admin = new HtmlTemplate(__DIR__ . "/templates/contact_admin.html",
			$this->dictionary);
		$source = new HtmlTemplate(__DIR__ . "/templates/contact_source.html",
			$this->dictionary);

		$box = new Container([new Row([
			$dividerOne, $admin, $dividerTwo, $source, $dividerOne
		])]);

		return [$box];
	}
}