<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/18/17
 * Time: 2:48 PM
 */

namespace bundesliga_tippspiel;
use chameleon_bootstrap\Container;
use chameleon_bootstrap\Row;
use cheetah\Match;


/**
 * Class Match
 * Page that displays information about a match
 * @package bundesliga_tippspiel
 */
class MatchPage extends Page {

	private $match;

	/**
	 * Match constructor.
	 */
	public function __construct() {
		parent::__construct(
			"@{MATCH_TITLE}", "@{MATCH_JUMBO_TITLE}", "match.php"
		);

		if ($this->match !== null) {
			/** @noinspection PhpUndefinedFieldInspection */
			$jumboTitle = $this->match->homeTeam->name .
				"<br>VS.<br>" . $this->match->awayTeam->name;

			$jumbotron = new DefaultJumbotron($jumboTitle);
			$this->addInnerTemplate("JUMBOTRON", $jumbotron);
		}
	}

	/**
	 * Sets the content of the page
	 * @return array: The Page content
	 */
	protected function setContent(): array {

		$matchId = (int)$_GET["match_id"];
		$this->match = Match::fromId($this->db, $matchId);

		if ($this->match === null) {
			return [];
		} else {
			return [new Container([new Row([])])];
		}
	}
}