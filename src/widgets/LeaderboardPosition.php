<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/17/17
 * Time: 8:25 PM
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;


class LeaderboardPosition extends HtmlTemplate {

	public function __construct(int $position,
								string $username,
								int $points,
								string $colorClass) {
		parent::__construct(
			__DIR__ . "/templates/leaderboard_position.html", null
		);
		$this->bindParams([
			"POSITION" => (string)$position,
			"USERNAME" => $username,
			"POINTS" => (string)$points,
			"COLORCLASS" => $colorClass
		]);
	}

}