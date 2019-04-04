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
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.models.user_generated.Bet import Bet


def get_team_points_data(bets: Optional[List[Bet]] = None) \
        -> Dict[User, Dict[Team, int]]:
    """
    Generates inforation about the amount of points each user achieved
    betting on specific teams
    :param bets: The bets to analyze. If not provided, will analyze all bets
    :return: A dictionary mapping users to dictionaries mapping teams to points
    """
    stats = {}
    for user in User.query.all():
        stats[user] = {}
        for team in Team.query.all():
            stats[user][team] = 0

    if bets is None:
        bets = Bet.query.all()

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
    total_stats = {}

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
