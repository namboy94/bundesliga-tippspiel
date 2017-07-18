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
use chameleon\Form;
use cheetah\Bet;
use cheetah\Match;
use cheetah\SeasonManager;
use welwitschi\User;


/**
 * Class MatchdayBetForm
 * Form that lets a user bet on any match in a matchday
 * @package bundesliga_tippspiel
 */
class MatchdayBetForm extends Form {

	/**
	 * MatchdayBetForm constructor.
	 * @param Dictionary|null $dictionary: Dictionary used in translation
	 * @param User $user: The user accessing this form
	 * @param int|null $matchDay: The matchday to display
	 * @SuppressWarnings docBlocks
	 */
	public function __construct(
		? Dictionary $dictionary,
		User $user,
		? int $matchDay = null
	) {

		$db = Functions::getMysqli();
		$seasonManager = new SeasonManager($db);
		if ($matchDay === null) {
			$matchDay = $seasonManager->getCurrentMatchday();
		}

		$formElements = [];
		$matches = Match::getAllForMatchday($db, $matchDay);
		foreach ($matches as $match) {
			/** @noinspection PhpParamsInspection */
			array_push($formElements,
				new BetFormEntry($match, Bet::fromMatchAndUserId(
					$db, $match->id, $user->id)
				)
			);
		}

		$previous = "bets.php?matchday=" . (string)($matchDay - 1);
		$next = "bets.php?matchday=" . (string)($matchDay + 1);

		$previousArrow = $matchDay < 2 ? "" : "&lt;";
		$nextArrow =
			$matchDay >= $seasonManager->getMaxMatchday() ? "" : "&gt;";

		parent::__construct(
			$dictionary,
			"@{MATCHDAY_BETFORM_TITLE} " . (string)$matchDay,
			"actions/bet.php",
			$formElements
		);

		$this->bindParams([
			"PREVIOUS_LINK" => $previous,
			"NEXT_LINK" => $next,
			"LEFT_ARROW" => $previousArrow,
			"RIGHT_ARROW" => $nextArrow
		]);

		$this->changeTemplate(__DIR__ . "/templates/matchday_bets.html");
	}

}