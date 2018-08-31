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

from typing import Dict, Any
from bundesliga_tippspiel import db
from bundesliga_tippspiel.models.ModelMixin import ModelMixin


class Goal(ModelMixin, db.Model):
    """
    Model that describes the "goals" SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "goals"
    """
    The name of the table
    """

    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the match in which this goal was scored. Acts as a foreign key.
    """

    match = db.relationship(
        "Match", backref=db.backref("goals", lazy=True, cascade="all,delete")
    )
    """
    The match in which this goal was scored.
    """

    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the player that scored this goal. Acts as a foreign key.
    """

    player = db.relationship(
        "Player",
        backref=db.backref("goals", lazy=True, cascade="all,delete")
    )
    """
    The player that scored this goal.
    """

    minute = db.Column(db.Integer, nullable=False)
    """
    The minute in which the goal was scored
    """

    minute_et = db.Column(db.Integer, nullable=True, default=0)
    """
    This keeps track in which minute of extra time a goal was scored.
    """

    home_score = db.Column(db.Integer, nullable=False)
    """
    The home team's score after the goal was scored
    """

    away_score = db.Column(db.Integer, nullable=False)
    """
    The away team's score after the goal was scored
    """

    own_goal = db.Column(db.Boolean, nullable=False, default=False)
    """
    Indicates whether or not this goal was an own goal
    """

    penalty = db.Column(db.Boolean, nullable=False, default=False)
    """
    Indicates whether or not this goal was a penalty
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
            "match_id": self.match_id,
            "player_id": self.player_id,
            "minute": self.minute,
            "minute_et": self.minute_et,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "own_goal": self.own_goal,
            "penalty": self.penalty
        }
        if include_children:
            data["match"] = self.match.__json__(include_children)
            data["player"] = self.player.__json__(include_children)
        return data
