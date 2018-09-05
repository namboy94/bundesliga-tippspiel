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

from typing import List, Tuple, Dict
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction


def generate_leaderboard_data() \
        -> Tuple[int, Dict[str, Tuple[str, List[int]]]]:
    """
    Generates leaderboard data for the rankings chart
    :return: A tuple consisting of the matchday to display
             and the leaderboard data:
                 username: (colour, list of positions per matchday)
    """

    chart_colors = ["red", "blue", "yellow",
                    "green", "purple", "orange",
                    "brown", "black", "gray"]

    leaderboard_action = LeaderboardAction()
    current_matchday = leaderboard_action.resolve_and_check_matchday(-1)

    leaderboard_data = {}

    for matchday in range(1, current_matchday + 1):

        leaderboard_action.matchday = matchday
        leaderboard = leaderboard_action.execute()["leaderboard"]

        for index, (user, points) in enumerate(leaderboard):

            if user.username not in leaderboard_data:
                color = chart_colors[index % len(chart_colors)]
                leaderboard_data[user.username] = (color, [])

            position = index + 1
            leaderboard_data[user.username][1].append(position)

    return current_matchday, leaderboard_data
