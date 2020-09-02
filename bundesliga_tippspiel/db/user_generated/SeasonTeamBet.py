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
from puffotter.flask.base import db
from puffotter.flask.db.User import User
from puffotter.flask.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.db.match_data.Team import Team


class SeasonTeamBetType(Enum):
    """
    Class that specifies the various season team bets that are possible
    """
    MOST_GOALS_SCORED = "Die meisten Tore"
    LEAST_GOALS_SCORED = "Die wenigsten Gegentore"
    MOST_GOALS_CONCEDED = "Die meisten Gegentore"
    LEAST_GOALS_CONCEDED = "Die wenigsten Tore"
    MOST_OWN_GOALS = "Die meisten Eigentore"
    # MOST_YELLOW_CARDS = "Die meisten gelben Karten"
    # MOST_RED_CARDS = "Die meisten roten Karten"


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

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "bet_type",
            "season",
            name="unique_season_team_bet"
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
    The ID of the user associated with this bet
    """

    user: User = db.relationship(
        "User", backref=db.backref("season_team_bets", cascade="all, delete")
    )
    """
    The user associated with this bet
    """

    season: int = db.Column(db.Integer, nullable=False)
    """
    The season of the season bet
    """

    team_id: int = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )
    """
    The ID of the team the user bet on.
    """

    team: Team = db.relationship(
        "Team", back_populates="season_team_bets"
    )
    """
    The team the user bet on.
    """

    bet_type: SeasonTeamBetType = db.Column(
        db.Enum(SeasonTeamBetType), nullable=False
    )
    """
    The type of the bet
    """
