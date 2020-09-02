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

from typing import Optional, List, Dict, Tuple
from puffotter.flask.db.User import User
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction


def get_team_points_data(bets: Optional[List[Bet]] = None) \
        -> Dict[User, Dict[Team, int]]:
    """
    Generates inforation about the amount of points each user achieved
    betting on specific teams
    :param bets: The bets to analyze. If not provided, will analyze all bets
    :return: A dictionary mapping users to dictionaries mapping teams to points
    """
    stats: Dict[User, Dict[Team, int]] = {}
    for user in User.query.filter_by(confirmed=True):
        stats[user] = {}
        for team in GetTeamAction().execute()["teams"]:
            stats[user][team] = 0

    if bets is None:
        bets = Bet.query.join(Match).filter(Match.season == Config.season())\
            .all()

    for bet in bets:
        for team in [bet.match.home_team, bet.match.away_team]:
            stats[bet.user][team] += bet.evaluate(when_finished=True)

    return stats


def get_total_points_per_team(bets: Optional[List[Bet]] = None) \
        -> Dict[Team, int]:
    """
    Retrieves the total amount of points achieved by betting on individual
    teams
    :param bets: The bets to analyze. If not provided, will analyze all bets
    :return: A dictionary mapping the teams to the points achieved by users
             betting on them
    """

    all_stats = get_team_points_data(bets)
    total_stats: Dict[Team, int] = {}

    for _, team_stats in all_stats.items():
        for team, points in team_stats.items():

            if team not in total_stats:
                total_stats[team] = 0
            total_stats[team] += points

    return total_stats


def generate_team_points_table(team_points: Dict[Team, int]) \
        -> List[Tuple[Team, int]]:
    """
    Generates a sorted list of tuples of teams and their points.
    :param team_points: The points achieved by the teams
    :return: The sorted list of tuples
    """
    table = []
    for team, points in team_points.items():
        table.append((team, points))
    table.sort(key=lambda x: x[1], reverse=True)
    return table


def generate_points_distributions(bets: Optional[List[Bet]] = None) \
        -> Dict[User, Dict[int, int]]:
    """
    Generates a distribution detailing how often a given amount of points
    a user earned while betting
    :param bets: The bets to analyze. If not provided, will analyze all bets
    :return: A dictionary mapping users to point amounts to their
             appearance count
    """
    if bets is None:
        bets = Bet.query.join(Match).filter(Match.season == Config.season()) \
            .all()
        bets = list(filter(lambda x: x.match.finished, bets))

    distribution: Dict[User, Dict[int, int]] = {}
    for user in User.query.filter_by(confirmed=True):
        distribution[user] = {}

    for bet in bets:
        points = bet.evaluate(True)
        if points not in distribution[bet.user]:
            distribution[bet.user][points] = 0
        distribution[bet.user][points] += 1

    return distribution


def create_participation_ranking(bets: Optional[List[Bet]] = None) \
        -> List[Tuple[User, str]]:
    """
    Creates a ranking of user's participation percentages
    :param bets: The bets to analyze. If not provided, will analyze all bets
    :return: A sorted list of tuples detailing the participation ranking
    """
    matches = Match.query.filter_by(season=Config.season()).all()
    matches = list(filter(lambda x: x.finished, matches))

    if bets is None:
        bets = Bet.query.join(Match).filter(Match.season == Config.season()) \
            .all()
        bets = list(filter(lambda x: x.match.finished, bets))

    participation_stats = {}
    for user in User.query.filter_by(confirmed=True):
        participation_stats[user] = 0

    for bet in bets:
        participation_stats[bet.user] += 1

    ranking = []
    for user, betcount in participation_stats.items():
        try:
            percentage = int((betcount / len(matches)) * 100)
        except ZeroDivisionError:
            percentage = 100
        ranking.append((user, percentage))

    ranking.sort(key=lambda x: x[1], reverse=True)
    return list(map(
        lambda x: (x[0], "{}%".format(x[1])),
        ranking
    ))


def create_point_average_ranking(bets: Optional[List[Bet]] = None) \
        -> List[Tuple[User, str]]:
    """
    Creates a ranking of points averages
    :param bets: The bets to analyze
    :return: The ranking
    """
    distribution = generate_points_distributions(bets)
    averages = []

    for user, points_distrib in distribution.items():
        total_points = 0
        count = 0

        for value, occurences in points_distrib.items():
            total_points += (value * occurences)
            count += occurences

        try:
            ratio = total_points / count
        except ZeroDivisionError:
            ratio = 0

        averages.append((user, ratio))

    averages.sort(key=lambda x: x[1], reverse=True)
    return list(map(
        lambda x: (x[0], "%.2f" % x[1]),
        averages
    ))
