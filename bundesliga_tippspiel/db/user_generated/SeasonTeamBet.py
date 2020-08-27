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

from enum import Enum
from typing import Dict, Any
from puffotter.flask.base import db
from puffotter.flask.db.ModelMixin import ModelMixin


class SeasonTeamBetType(Enum):
    """
    Class that specifies the various season team bets that are possible
    """
    MOST_GOALS_SCORED = "most goals scored"
    LEAST_GOALS_SCORED = "least goals scored"
    MOST_GOALS_CONCEDED = "most goals conceded"
    LEAST_GOALS_CONCEDED = "least goals conceded"
    MOST_OWN_GOALS = "most own goals"
    MOST_YELLOW_CARDS = "most yellow cards"
    MOST_RED_CARDS = "most red cards"


class SeasonTeamBet(ModelMixin, db.Model):
    """
    Model that describes the 'season_team_bets' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "season_team_bets"
    """
    The name of the table
    """

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            "users.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the user associated with this season team bet
    """

    user = db.relationship(
        "User", backref=db.backref("bets", lazy=True, cascade="all,delete")
    )
    """
    The user associated with this season team bet
    """

    season: db.Column(db.Integer, nullable=False)
    """
    The season of the season bet
    """

    bet_value: db.Column(db.Integer, nullable=False)
    """
    The value of the bet
    """

    bet_type = db.Column(db.Enum(SeasonTeamBetType), nullable=False)
    """
    The type of the bet
    """

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "season": self.season,
            "bet_value": self.bet_value,
            "bet_type": self.bet_type.value
        }
        if include_children:
            data["user"] = self.user.__json__(include_children)
        return data
