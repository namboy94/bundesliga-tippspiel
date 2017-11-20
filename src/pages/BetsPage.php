<?php
/**
 * Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>
 *
 * This file is part of bundesliga-tippspiel.
 *
 * bundesliga-tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga-tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga-tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel;
use champlates_bootstrap\Col;
use champlates_bootstrap\Container;
use champlates_bootstrap\Row;


/**
 * Class Bets
 * The Bets page, displaying the current matchday's bets with buttons
 * to the next and previous matchdays
 * @package bundesliga_tippspiel
 */
class BetsPage extends Page {

	/**
	 * Bets constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{BETS_TITLE}",
			"@{BETS_JUMBO_TITLE}",
			"bets.php",
			true
		);
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {

		$matchday = isset($_GET["matchday"]) ? (int)$_GET["matchday"] : null;
		$form = new MatchdayBetForm($this->dictionary, $this->user, $matchday);

		return [new Row([new Col([$form], 12)])];
	}
}