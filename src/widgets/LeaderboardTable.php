<?php

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use cheetah\LeaderBoard;
use welwitschi\User;


/**
 * Class LeaderboardTable
 * Displays a Table of users sorted by their points in the betting game
 * @package bundesliga_tippspiel
 */
class LeaderboardTable extends HtmlTemplate {

	/**
	 * LeaderboardTable constructor.
	 * @param Dictionary|null $dictionary: DIctionary used for translation
	 * @param User $activeUser: The active user, who will be marked in
	 *                          the ranking table
	 */
	public function __construct(
		? Dictionary $dictionary,
		User $activeUser
	) {
		parent::__construct(
			__DIR__ . "/templates/leaderboard_table.html", $dictionary
		);

		$leaderboard = new LeaderBoard(Functions::getMysqli());
		$ranking = $leaderboard->generateRanking();

		$positions = [];

		foreach ($ranking as $position => $userData) {
			$user = $userData[0];
			$points = $userData[1];

			if ($user->id === $activeUser->id) {
				$colorClass = "info";
			} elseif ($position === 1) {
				$colorClass = "success";
			} elseif ($position === count($ranking)) {
				$colorClass = "danger";
			} else {
				$colorClass = "default";
			}

			$positionElement = new LeaderboardPosition(
				$position, $user->username, $points, $colorClass
			);
			array_push($positions, $positionElement);
		}

		$this->addCollectionFromArray("POSITIONS", $positions);

	}
}