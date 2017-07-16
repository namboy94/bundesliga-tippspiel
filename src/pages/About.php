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
use chameleon_bootstrap\Col;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;


/**
 * Class About
 * The About/Impressum Page
 * @package bundesliga_tippspiel
 */
class About extends Page {

	/**
	 * About constructor.
	 */
	public function __construct() {

		$container = new Container(
			[new Row(
				[new Col(
					[new Html(
						"@{ABOUT_TEXT}")],
					10)]
			)]
		);
		parent::__construct(
			"@{ABOUT_TITLE}",
			"@{ABOUT_JUMBO_TITLE}",
			"about.php",
			[$container]);
	}

}