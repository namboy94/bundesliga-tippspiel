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


/**
 * Class LeaderboardPosition
 * A Position in the LeaderboardTable
 * @package bundesliga_tippspiel
 */
class LeaderboardPosition extends HtmlTemplate {

	/**
	 * LeaderboardPosition constructor.
	 * @param int $position: The position of the user inside the table
	 * @param string $username: The name of the user
	 * @param int $points: The amount of points the user has
	 * @param string $colorClass: Which colour to display this user's entry in
	 */
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