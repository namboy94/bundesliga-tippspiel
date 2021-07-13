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

from typing import Tuple, List, Dict
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.db.User import User


class LeaderboardEntry(ModelMixin, db.Model):
    """
    Model that describes the 'leaderboard_entries' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "leaderboard_entries"

    league: int = db.Column(db.String(255), primary_key=True)
    season: int = db.Column(db.Integer, primary_key=True)
    matchday: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    points: int = db.Column(db.Integer, nullable=False)
    position: int = db.Column(db.Integer, nullable=False)
    no_bot_position: int = db.Column(db.Integer, nullable=False)
    previous_position: int = db.Column(db.Integer, nullable=False)
    no_bot_previous_position: int = db.Column(db.Integer, nullable=False)

    user: User = db.relationship(
        "User",
        backref=db.backref("leaderboard_entries", cascade="all, delete")
    )

    def get_position_info(self, include_bots: bool) -> Tuple[int, int]:
        """
        Retrieves position info
        :param include_bots: Whether or not to include bots in the ranking
        :return: Current Position, Previous Position
        """
        current = self.position if include_bots else self.no_bot_position
        previous = self.previous_position \
            if include_bots else self.no_bot_previous_position
        return current, previous

    def get_tendency(self, include_bots: bool) -> str:
        """
        Calculates the position tendency
        :param include_bots: Whether or not to include bots
        :return: The tendency as a string (example '+2')
        """
        current, previous = self.get_position_info(include_bots)
        tendency = previous - current
        if tendency < 0:
            return str(tendency)
        elif tendency > 0:
            return f"+{tendency}"
        else:
            return "-"

    def get_tendency_class(self, include_bots: bool) -> str:
        """
        Calculates the tendency and returns the corrsponding CSS class
        :param include_bots: Whether or not to include bots
        :return: The tendency CSS class name
        """
        current, previous = self.get_position_info(include_bots)

        if current < previous:
            return "chevron-circle-up"
        elif current > previous:
            return "chevron-circle-down"
        else:
            return "minus-circle"

    @classmethod
    def load_history(cls, league: str, season: int, matchday: int) -> \
            List[Tuple[User, List["LeaderboardEntry"]]]:
        """
        Loads the history for the previous matches in a season for each user
        :param league: The league for which to retrieve the history
        :param season: The season for which to retrieve the history
        :param matchday: The matchday for which to retrieve the history
        :return: The history as a list of tuples of users and a list of
                 the corresponding LeaderboardEntry objects.
                 Sorted by current position
        """
        entries: List[LeaderboardEntry] = [
            x for x in
            LeaderboardEntry.query.filter_by(
                league=league,
                season=season
            ).options(db.joinedload(LeaderboardEntry.user)).all()
            if x.matchday <= matchday
        ]
        entries.sort(key=lambda x: x.matchday)

        history_dict: Dict[int, List[LeaderboardEntry]] = {}
        for entry in entries:
            if entry.user_id not in history_dict:
                history_dict[entry.user_id] = []
            history_dict[entry.user_id].append(entry)

        history_list = [
            (history[-1].user, history)
            for _, history in history_dict.items()
        ]
        history_list.sort(key=lambda x: x[1][-1].position)
        return history_list
