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

from typing import List, TYPE_CHECKING
from puffotter.flask.base import db
from puffotter.flask.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.db.match_data.Team import Team
if TYPE_CHECKING:  # pragma: no cover
    from bundesliga_tippspiel.db.match_data.Goal import Goal


class Player(ModelMixin, db.Model):
    """
    Model that describes the "players" SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "players"
    """
    The name of the database table
    """

    team_id: int = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )
    """
    The ID of the team the player is affiliated with.
    Acts as a foreign key to the 'teams' table.
    """

    team: Team = db.relationship("Team", back_populates="players")
    """
    The team the player is affiliated with.
    """

    name: str = db.Column(db.String(255), nullable=False)
    """
    The name of the player
    """

    goals: List["Goal"] = db.relationship(
        "Goal", back_populates="player", cascade="all, delete"
    )
    """
    The goals the player scored.
    """
