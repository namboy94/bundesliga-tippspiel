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
from puffotter.flask.db.User import User
from bundesliga_tippspiel.db.match_data.Team import Team


class SeasonPositionBet(ModelMixin, db.Model):
    """
    Model that describes the 'season_position_bets' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "season_position_bets"
    """
    The name of the table
    """

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "team_id",
            "season",
            name="unique_position_bet"
        ),
    )
    """
    Table arguments for unique constraints
    """

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    """
    The ID of the user associated with this season position bet
    """

    user: User = db.relationship(
        "User",
        backref=db.backref("season_position_bets", cascade="all, delete")
    )
    """
    The user associated with this season position bet
    """

    team_id: int = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )
    """
    The ID of the team the position bet is for.
    """

    team: Team = db.relationship(
        "Team", back_populates="season_position_bets"
    )
    """
    The team the position bet is for.
    """

    season: int = db.Column(db.Integer, nullable=False)
    """
    The season of the season bet
    """

    position: int = db.Column(db.Integer, nullable=False)
    """
    The position of the team in the table
    """
