"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Tuple, List, Dict, Union, Any
from jerrycan.db.User import User
from bundesliga_tippspiel.db import Team, LeaderboardEntry
from bundesliga_tippspiel.utils.collections.StatsGenerator import \
    StatsGenerator


class UserStatsGenerator(StatsGenerator):
    """
    Class that generates statistics for a single user
    """

    def __init__(
            self,
            league: str,
            season: int,
            matchday: int,
            user: User,
            include_bots: bool
    ):
        """
        Initializes the UserStatsGenerator object
        :param league: The league for which to generate statistics
        :param season: The season for which to generate statistics
        :param matchday: The matchday for which to generate statistics
        :param user: The user for which to generate statistics
        :param include_bots: Whether or not to include bots
        """
        super().__init__(league, season, matchday, include_bots)
        self.user = user
        histories = [
            history for history_user, history in self.history
            if history_user.id == self.user.id
        ]
        self.user_history = [] if len(histories) == 0 else histories[0]
        self.per_day_user_history: Dict[int, LeaderboardEntry] = {
            x.matchday: x for x in self.user_history
        }
        self.user_bets = [x for x in self.bets if x.user_id == self.user.id]

    def get_user_position(self) -> int:
        """
        :return: The current position of the user
        """
        history = self.per_day_user_history.get(self.selected_matchday)
        if history is None:
            return 0
        else:
            return history.get_position_info(self.include_bots)[0]

    def get_user_first_half_position(self) -> int:
        """
        :return: The user's position in the first half of the season
        """
        return self.extract_user_position(self.get_first_half_ranking())

    def get_user_second_half_position(self) -> int:
        """
        :return: The user's position in the second half of the season
        """
        return self.extract_user_position(self.get_second_half_ranking())

    def get_user_best_position(self) -> int:
        """
        :return: The user's best position during the season
        """
        best = len(self.users)
        for history_item in self.user_history:
            position = history_item.get_position_info(self.include_bots)[0]
            best = min(position, best)
        return best

    def get_user_worst_position(self) -> int:
        """
        :return: The user's worst position during the season
        """
        worst = 1
        for history_item in self.user_history:
            position = history_item.get_position_info(self.include_bots)[0]
            worst = max(position, worst)
        return worst

    def get_user_points(self) -> int:
        """
        :return: The user's current point total
        """
        history = self.per_day_user_history.get(self.selected_matchday)
        return 0 if history is None else history.points

    def get_user_bet_count(self) -> int:
        """
        :return: The amount of bets the user has placed
        """
        return len(self.user_bets)

    def get_user_betting_average(self) -> float:
        """
        :return: The average points per bet of the user
        """
        points = [bet.points for bet in self.user_bets]
        total = len(points)
        return 0.0 if total == 0 else sum(points) / total

    def get_user_participation(self) -> int:
        """
        :return: The user's participation up to this point
        """
        ranking = self.get_participation_ranking()
        try:
            return [x for x in ranking if x[0].id == self.user.id][0][1]
        except IndexError:
            return 0

    def get_user_correct_bets(self) -> int:
        """
        :return: The amount of correct bets for this user
        """
        ranking = self.get_correct_bets_ranking()
        try:
            return [x for x in ranking if x[0].id == self.user.id][0][1]
        except IndexError:
            return 0

    def get_user_wrong_bets(self) -> int:
        """
        :return: The amount of wrong bets for this user
        """
        ranking = self.get_wrong_bets_ranking()
        try:
            return [x for x in ranking if x[0].id == self.user.id][0][1]
        except IndexError:
            return 0

    def get_user_best_team(self) -> Tuple[Team, float]:
        """
        :return: The team this user has achieved the most points for so far
        """
        return self.get_user_average_points_per_team()[0]

    def get_user_worst_team(self) -> Tuple[Team, float]:
        """
        :return: The team this user has achieved the least points for so far
        """
        return self.get_user_average_points_per_team()[-1]

    def get_user_average_points_per_team(self) -> List[Tuple[Team, float]]:
        """
        :return: The average points per team for this user
        """
        return self.calculate_average_points_per_team(self.user_bets)

    def extract_user_position(self, ranking: List[Tuple[User, Any]]) -> int:
        """
        Extracts the user's position from a ranking
        :return: The position in the ranking
        """
        try:
            order = [x[0].id for x in ranking]
            return order.index(self.user.id) + 1
        except ValueError:
            return 0

    def get_user_points_distribution(self) -> Dict[int, int]:
        """
        :return: A distribution of points for all possible point results
        """
        return self.calculate_point_distribution_per_user()[self.user]
