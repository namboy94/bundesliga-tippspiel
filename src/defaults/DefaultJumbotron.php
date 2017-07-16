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
use chameleon\TitleJumboTron;


/**
 * Class DefaultJumbotron
 * The Default Jumbotron to display on the top of the page
 * @package bundesliga_tippspiel
 */
class DefaultJumbotron extends TitleJumboTron {

	/**
	 * DefaultJumbotron constructor.
	 * @param string $title: The title of the Jumbotron
	 */
	public function __construct(string $title) {
		parent::__construct(
			new DefaultDictionary(),
			$title,
			"resources/images/grass.jpg");
		$this->changeTemplate(__DIR__ . "/templates/default_jumbotron.html");
	}
}