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
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.db import SeasonWinner, LeaderboardEntry, \
    DisplayBotsSettings, MatchdayWinner, UserProfile


class Leaderboard:
    """
    Class that encapsulates a leaderboard
    """

    def __init__(
            self,
            league: str,
            season: int,
            matchday: int,
            include_bots: bool
    ):
        """
        Initializes the leaerboard object
        :param league: The league of the leaderboard
        :param season: The season of the leaderboard
        :param matchday: The matchday of the leaderboard
        :param include_bots: Whether or not to include bots
        """
        self.league = league
        self.season = season
        self.matchday = matchday
        self.include_bots = include_bots

        self.season_winners: Dict[int, List[str]] = {}
        for season_winner in SeasonWinner.query.filter_by(league=league).all():
            user_id = season_winner.user_id
            winner_season = season_winner.season_string
            if user_id not in self.season_winners:
                self.season_winners[user_id] = []
            self.season_winners[user_id].append(winner_season)
        self.matchday_winners: Dict[int, List[int]] = {}
        for matchday_winner in MatchdayWinner.query.filter_by(
                league=league, season=season
        ).all():
            user_id = matchday_winner.user_id
            winner_matchday = matchday_winner.matchday
            if user_id not in self.matchday_winners:
                self.matchday_winners[user_id] = []
            self.matchday_winners[user_id].append(winner_matchday)

        self.ranking: List[LeaderboardEntry] = \
            LeaderboardEntry.query.filter_by(
                league=league,
                season=season,
                matchday=matchday
            ).options(db.joinedload(LeaderboardEntry.user)
                      .subqueryload(User.profile)
                      .subqueryload(UserProfile.favourite_team)).all()
        self.ranking.sort(key=lambda x: x.position)
        self.history: List[Tuple[User, List["LeaderboardEntry"]]] \
            = LeaderboardEntry.load_history(league, season, matchday)

        if not include_bots:
            self.ranking = [
                x for x in self.ranking
                if DisplayBotsSettings.bot_symbol() not in x.user.username
            ]
            self.history = [
                x for x in self.history
                if DisplayBotsSettings.bot_symbol() not in x[0].username
            ]

    def ranking_to_table_data(self) -> List[Tuple[
        int, str, str, User, List[str], List[int], int
    ]]:
        """
        Converts the leaderboard into a format that can easily be entered
        into a HTML table
        :return: The data as tuple with the following attributes:
                    - position
                    - tendency (example: +2 or -3 etc.)
                    - tendency-class
                    - user
                    - previous season wins
                    - previous matchday wins
                    - points
        """
        table_data = []
        for item in self.ranking:
            table_data.append((
                item.get_position_info(self.include_bots)[0],
                item.get_tendency(self.include_bots),
                item.get_tendency_class(self.include_bots),
                item.user,
                self.season_winners.get(item.user_id, []),
                self.matchday_winners.get(item.user_id, []),
                item.points
            ))
        return table_data

    def matchday_ranking_to_table_data(self) -> List[Tuple[
        int, None, None, User, List[str], List[int], int
    ]]:
        """
        Calculates the leaderboard ranking to table data for the current
        matchday only
        :return: The data as tuple with the following attributes:
                    - position
                    - tendency (None in this case)
                    - tendency-class (None in this case)
                    - user
                    - previous season wins (Empty list in this case)
                    - The matchday wins for the current mtchday only
                    - points on this matchday
        """
        table_data: List[Tuple[User, List[int], int]] = []
        matchday_winners = [
            user_id for user_id, matchdays in self.matchday_winners.items()
            if self.matchday in matchdays
        ]

        user_histories = dict(self.history)
        for item in self.ranking:
            points = item.points
            if item.matchday > 1:
                previous = user_histories[item.user][-2]
                points -= previous.points

            table_data.append((
                item.user,
                [self.matchday] if item.user_id in matchday_winners else [],
                points
            ))
        table_data.sort(key=lambda x: x[2], reverse=True)
        table: List[Tuple[int, None, None, User, List[str], List[int], int]] \
            = []

        for i, data in enumerate(table_data):
            empty: List[str] = []
            table.append((
                i + 1,
                None,
                None,
                data[0],
                empty,
                data[1],
                data[2]
            ))
        return table

    def history_to_chart_data(self) -> List[Tuple[str, str, List[int]]]:
        """
        Creates data for the ranking chart
        :return: The data to be used by the javascript chart
        """
        chart_colours = ["red", "blue", "yellow",
                         "green", "purple", "orange",
                         "brown", "black", "gray"]

        chart_data = []

        for i, (user, user_history) in enumerate(self.history):
            chart_colour = chart_colours[i % len(chart_colours)]
            user_positions = []
            for item in user_history:
                position = item.get_position_info(self.include_bots)[0]
                user_positions.append(position)
            chart_data.append((user.username, chart_colour, user_positions))

        return chart_data
