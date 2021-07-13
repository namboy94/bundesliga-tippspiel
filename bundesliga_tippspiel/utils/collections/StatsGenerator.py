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

from typing import Dict, List, Tuple
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.db import LeaderboardEntry, Team, Bet, Match, \
    DisplayBotsSettings
from bundesliga_tippspiel.utils.collections.Leaderboard import Leaderboard
from bundesliga_tippspiel.utils.matchday import get_matchday_info


class StatsGenerator(Leaderboard):
    """
    Class that generates various statistics.
    Uses the Leaderboard class as base to calculate the statistics
    """

    def __init__(
            self,
            league: str,
            season: int,
            matchday: int,
            include_bots: bool
    ):
        """
        Initializes the StatsGenerator object.
        Loads the required data from the database
        :param league: The league for which to generate stats
        :param season: The season for which to generate stats
        :param matchday: The matchday for which to generate stats
        :param include_bots: Whether or not to include bots
        """
        self.selected_matchday = matchday
        self.max_matchday = get_matchday_info(league, season)[1]
        self.midpoint = int(self.max_matchday / 2)
        super().__init__(league, season, matchday, include_bots)

        self.per_day_history: Dict[int, Dict[User, LeaderboardEntry]] = {}
        for user, user_history in self.history:
            for entry in user_history:
                if entry.matchday not in self.per_day_history:
                    self.per_day_history[entry.matchday] = {}
                self.per_day_history[entry.matchday][user] = entry
        self.matches = [
            x for x in Match.query.filter_by(
                season=season, league=league
            ).options(db.joinedload(Match.bets).subqueryload(Bet.user)).all()
            if x.matchday <= self.selected_matchday
        ]
        self.bets = []
        for match in self.matches:
            for bet in [x for x in match.bets if x.points is not None]:
                is_bot = DisplayBotsSettings.bot_symbol() in bet.user.username
                if bet.points is not None and (include_bots or not is_bot):
                    self.bets.append(bet)

        self.teams = Team.get_teams_for_season(league, season)
        self.users = [
            x for x in
            User.query.filter_by(confirmed=True).all()
            if include_bots or
            DisplayBotsSettings.bot_symbol() not in x.username
        ]

    def get_first_half_ranking(self) -> List[Tuple[User, int]]:
        """
        :return: A ranking for the first half of the season
        """
        matchday = min(self.selected_matchday, self.midpoint)
        return list(sorted([
            (user, position.points)
            for user, position
            in self.per_day_history.get(matchday, {}).items()
        ], key=lambda x: x[1], reverse=True))

    def get_second_half_ranking(self) -> List[Tuple[User, int]]:
        """
        :return: A ranking for the second half of the season
        """
        first_half = self.get_first_half_ranking()
        if self.selected_matchday <= self.midpoint:
            return [(user, 0) for user, _ in first_half]
        else:
            first_half_mapping = {user: points for user, points in first_half}
            return list(sorted([
                (user, position.points - first_half_mapping[user])
                for user, position
                in self.per_day_history.get(self.selected_matchday, {}).items()
            ], key=lambda x: x[1], reverse=True))

    def get_correct_bets_ranking(self) -> List[Tuple[User, int]]:
        """
        :return: A ranking for the amount of correct bets for each user
        """
        return list(sorted([
            (user, points[Bet.MAX_POINTS])
            for user, points
            in self.calculate_point_distribution_per_user().items()
        ], key=lambda x: x[1], reverse=True))

    def get_wrong_bets_ranking(self) -> List[Tuple[User, int]]:
        """
        :return: A ranking for the amount of incorrect bets for each user
        """
        return list(sorted([
            (user, points[0])
            for user, points
            in self.calculate_point_distribution_per_user().items()
        ], key=lambda x: x[1], reverse=True))

    def get_points_average_ranking(self) -> List[Tuple[User, float]]:
        """
        :return: A ranking for the average points per bet for each user
        """
        per_user: Dict[User, List[int]] = {user: [] for user in self.users}
        for bet in self.bets:
            per_user[bet.user].append(bet.points)
        ranking = []
        for user, points in per_user.items():
            total = len(points)
            avg = 0.0 if total == 0 else sum(points) / total
            ranking.append((user, avg))
        return list(sorted(ranking, key=lambda x: x[1], reverse=True))

    def get_participation_ranking(self) -> List[Tuple[User, int]]:
        """
        :return: A ranking for the participation rate for each user
        """
        total = len(self.matches)
        participation = {user: 0 for user in self.users}
        for match in self.matches:
            for bet in match.bets:
                is_bot = DisplayBotsSettings.bot_symbol() in bet.user.username
                if self.include_bots or not is_bot:
                    participation[bet.user] += 1
        return list(sorted([
            (user, 0 if total == 0 else int(100 * (count / total)))
            for user, count in participation.items()
        ], key=lambda x: x[1], reverse=True))

    def get_points_distribution(self) -> Dict[int, int]:
        """
        :return: A distribution of points for all possible point results
        """
        distribution = {x: 0 for x in Bet.POSSIBLE_POINTS}
        for bet in self.bets:
            distribution[bet.points] += 1
        return distribution

    def get_average_points_per_team(self) -> List[Tuple[Team, float]]:
        """
        :return: A ranking for the average points achieved by team
        """
        return self.calculate_average_points_per_team(self.bets)

    def calculate_point_distribution_per_user(self) \
            -> Dict[User, Dict[int, int]]:
        """
        Calculates the points distribution for each user
        :return: {user: {points: count}}
        """
        per_user = {user: {
            x: 0 for x in Bet.POSSIBLE_POINTS
        } for user in self.users}

        for bet in self.bets:
            per_user[bet.user][bet.points] += 1
        return per_user

    def calculate_average_points_per_team(
            self, bets: List[Bet]
    ) -> List[Tuple[Team, float]]:
        """
        Calculates the average points per team
        :param bets: The bets to use to calculate the values
        :return: A ranking of the average points per team
        """
        team_map = {x.abbreviation: x for x in self.teams}
        points: Dict[str, List[int]] = {x.abbreviation: [] for x in self.teams}
        for bet in bets:
            for team in [
                bet.home_team_abbreviation,
                bet.away_team_abbreviation
            ]:
                points[team].append(bet.points)
        ranking = []
        for team_name, results in points.items():
            total = len(results)
            avg = 0.0 if total == 0 else sum(results) / total
            team = team_map[team_name]
            ranking.append((team, avg))
        return list(sorted(ranking, key=lambda x: x[1], reverse=True))
