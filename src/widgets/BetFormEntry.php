<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/18/17
 * Time: 10:09 AM
 */

namespace bundesliga_tippspiel;
use chameleon\HtmlTemplate;
use cheetah\Bet;
use cheetah\Match;


/**
 * Class BetFormEntry
 * A Bet Form for a single match
 * @package bundesliga_tippspiel
 */
class BetFormEntry extends HtmlTemplate {

	/**
	 * BetFormEntry constructor.
	 * @param Match $match: The match to display
	 * @param Bet|null $bet: Optionally provides previous bet data
	 * @param bool $small: Indicates if this orm will be small or not
	 */
	public function __construct(
		Match $match, ? Bet $bet, bool $small = false) {

		parent::__construct(__DIR__ . "/templates/bet_form_entry.html", null);

		$disabled = $match->hasStarted() ? "disabled" : "";
		if ($bet !== null) {
			$homeDefault = (string)$bet->homeScore;
			$awayDefault = (string)$bet->awayScore;
		} else {
			$homeDefault = "";
			$awayDefault = "";
		}

		if ($small) {
			$inputSize = 2;
			$nameSize = 4;
			$homeName = $match->homeTeam->shortname;
			$awayName = $match->awayTeam->shortname;
		} else {
			$inputSize = 1;
			$nameSize = 5;
			$homeName = $match->homeTeam->name;
			$awayName = $match->awayTeam->name;
		}

		$this->bindParams([
			"HOME_ID" => $match->homeTeam->id,
			"AWAY_ID" => $match->awayTeam->id,
			"HOME_NAME" => $homeName,
			"AWAY_NAME" => $awayName,
			"HOME_ICON" => $match->homeTeam->icon,
			"AWAY_ICON" => $match->awayTeam->icon,
			"MATCH_ID" => $match->id,
			"DISABLED" => $disabled,
			"HOME_DEFAULT" => $homeDefault,
			"AWAY_DEFAULT" => $awayDefault,
			"INPUT_SIZE" => $inputSize,
			"NAME_SIZE" => $nameSize
		]);
	}
}