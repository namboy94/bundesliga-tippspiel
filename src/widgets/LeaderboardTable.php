<?php

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use cheetah\LeaderBoard;
use welwitschi\User;


class LeaderboardTable extends HtmlTemplate {

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
			} elseif ($position == 1) {
				$colorClass = "success";
			} elseif ($position == count($ranking)) {
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