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

from puffotter.flask.base import db
from puffotter.flask.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Player import Player


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

    match_id: int = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )
    """
    The ID of the match in which this goal was scored. Acts as a foreign key.
    """

    match: Match = db.relationship("Match", back_populates="goals")
    """
    The match in which this goal was scored.
    """

    player_id: int = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )
    """
    The ID of the player that scored this goal. Acts as a foreign key.
    """

    player: Player = db.relationship(
        "Player",
        back_populates="goals"
    )
    """
    The player that scored this goal.
    """

    minute: int = db.Column(db.Integer, nullable=False)
    """
    The minute in which the goal was scored
    """

    minute_et: int = db.Column(db.Integer, nullable=True, default=0)
    """
    This keeps track in which minute of extra time a goal was scored.
    """

    home_score: int = db.Column(db.Integer, nullable=False)
    """
    The home team's score after the goal was scored
    """

    away_score: int = db.Column(db.Integer, nullable=False)
    """
    The away team's score after the goal was scored
    """

    own_goal: bool = db.Column(db.Boolean, nullable=False, default=False)
    """
    Indicates whether or not this goal was an own goal
    """

    penalty: bool = db.Column(db.Boolean, nullable=False, default=False)
    """
    Indicates whether or not this goal was a penalty
    """
