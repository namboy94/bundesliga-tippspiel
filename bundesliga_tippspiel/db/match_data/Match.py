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

from datetime import datetime
from typing import TYPE_CHECKING, List
from puffotter.flask.base import db
from puffotter.flask.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.db.match_data.Team import Team
if TYPE_CHECKING:  # pragma: no cover
    from bundesliga_tippspiel.db.match_data.Goal import Goal
    from bundesliga_tippspiel.db.user_generated.Bet import Bet


class Match(ModelMixin, db.Model):
    """
    Model that describes the 'matches' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "matches"
    """
    The table name
    """

    __table_args__ = (
        db.UniqueConstraint(
            "home_team_id",
            "away_team_id",
            "season",
            name="unique_match"
        ),
    )
    """
    Table arguments for unique constraints
    """

    home_team_id: int = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )
    """
    The ID of the home team. Acts as a foreign key
    """

    home_team: Team = db.relationship(
        "Team", foreign_keys=[home_team_id]  # back_populates="matches"
    )
    """
    The home team.
    """

    away_team_id: int = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )
    """
    The ID of the away team. Acts as a foreign key
    """

    away_team: Team = db.relationship(
        "Team", foreign_keys=[away_team_id]  # back_populates="matches"
    )
    """
    The away team.
    """

    matchday: int = db.Column(db.Integer, nullable=False)
    """
    The match day of the match
    """

    home_current_score: int = db.Column(db.Integer, nullable=False)
    """
    The current score of the home team.
    """

    away_current_score: int = db.Column(db.Integer, nullable=False)
    """
    The current score of the away team.
    """

    home_ht_score: int = db.Column(db.Integer)
    """
    The score of the home team at half time
    """

    away_ht_score: int = db.Column(db.Integer)
    """
    The score of the away team at half time
    """

    home_ft_score: int = db.Column(db.Integer)
    """
    The final score of the home team
    """

    away_ft_score: int = db.Column(db.Integer)
    """
    The final score of the away team
    """

    kickoff: str = db.Column(db.String(255), nullable=False)
    """
    A string representing the kickoff time in UTC in the following format:
    YYYY-MM-DD:HH-mm-ss
    If the kickoff time is not known, it should be set to 'TBD'
    """

    started: bool = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has started yet
    """

    finished: bool = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has finished yet
    """

    season: int = db.Column(db.Integer, nullable=False)
    """
    The season of the match
    """

    goals: List["Goal"] = db.relationship(
        "Goal", back_populates="match", cascade="all, delete"
    )
    """
    The goals scored during this match
    """

    bets: List["Bet"] = db.relationship(
        "Bet", back_populates="match", cascade="all, delete"
    )
    """
    Bets placed on this match
    """

    @property
    def minute_display(self) -> str:
        """
        This generates a string for displaying the current match minute.
        Sadly, since OpenligaDB does not provide information on the current
        minute, this can only offer an approximation.
        :return: A formatted string displaying the current match minute
        """
        delta = (datetime.utcnow() - self.kickoff_datetime).total_seconds()
        delta = int(delta / 60)

        if self.finished:
            return "Ende"
        elif 0 <= delta <= 44:
            return "{}.".format(delta + 1)
        elif 45 <= delta < 47:  # buffer for ET
            return "45."
        elif 47 <= delta <= 64:
            return "HZ"
        elif 65 <= delta <= 109:
            return "{}.".format(delta - 65 + 1 + 45)
        elif delta >= 110:
            return "90."
        else:
            return "-"

    @property
    def current_score(self) -> str:
        """
        :return: The current score formatted as a string
        """
        return "{}:{}".format(self.home_current_score, self.away_current_score)

    @property
    def ht_score(self) -> str:
        """
        :return: The half time score formatted as a string
        """
        return "{}:{}".format(self.home_ht_score, self.away_ht_score)

    @property
    def ft_score(self) -> str:
        """
        :return: The full time score formatted as a string
        """
        return "{}:{}".format(self.home_ft_score, self.away_ft_score)

    @property
    def kickoff_datetime(self) -> datetime:
        """
        :return: A datetime object representing the kickoff time
        """
        return datetime.strptime(self.kickoff, "%Y-%m-%d:%H-%M-%S")

    @kickoff_datetime.setter
    def kickoff_datetime(self, kickoff: datetime):
        """
        Setter for the kickoff datetime
        :param kickoff: The new kickoff datetime
        :return: None
        """
        self.kickoff = kickoff.strftime("%Y-%m-%d:%H-%M-%S")
