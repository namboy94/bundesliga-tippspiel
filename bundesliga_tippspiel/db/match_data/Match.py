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

import pytz
from datetime import datetime
from typing import TYPE_CHECKING, List

from flask import url_for
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
if TYPE_CHECKING:  # pragma: no cover
    from bundesliga_tippspiel.db.match_data.Goal import Goal
    from bundesliga_tippspiel.db.user_generated.Bet import Bet
    from bundesliga_tippspiel.db.match_data.Team import Team


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

    league: str = db.Column(db.String(255), primary_key=True)
    season: int = db.Column(db.Integer, primary_key=True)
    matchday: int = db.Column(db.Integer, primary_key=True)
    home_team_abbreviation: str = db.Column(
        db.String(3),
        db.ForeignKey("teams.abbreviation"),
        primary_key=True,
    )
    away_team_abbreviation: str = db.Column(
        db.String(3),
        db.ForeignKey("teams.abbreviation"),
        primary_key=True
    )

    home_current_score: int = db.Column(db.Integer, nullable=False)
    away_current_score: int = db.Column(db.Integer, nullable=False)
    home_ht_score: int = db.Column(db.Integer)
    away_ht_score: int = db.Column(db.Integer)
    home_ft_score: int = db.Column(db.Integer)
    away_ft_score: int = db.Column(db.Integer)
    kickoff: str = db.Column(db.String(255), nullable=False)
    started: bool = db.Column(db.Boolean, nullable=False)
    finished: bool = db.Column(db.Boolean, nullable=False)

    home_team: "Team" = db.relationship(
        "Team", foreign_keys=[home_team_abbreviation],
    )
    away_team: "Team" = db.relationship(
        "Team", foreign_keys=[away_team_abbreviation]
    )
    goals: List["Goal"] = db.relationship("Goal", cascade="all, delete")
    bets: List["Bet"] = db.relationship("Bet", cascade="all, delete")

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

    @property
    def kickoff_local_datetime(self) -> datetime:
        """
        :return: A datetime object representing the kickoff time in local time
        """
        return self.kickoff_datetime.astimezone(pytz.timezone("europe/berlin"))

    @property
    def kickoff_time_string(self) -> str:
        """
        :return: A string representing the kickoff time
        """
        return self.kickoff_local_datetime.strftime("%H:%M")

    @property
    def kickoff_date_string(self) -> str:
        """
        :return: A string representing the kickoff date
        """
        return self.kickoff_local_datetime.strftime("%d. %m. %Y")

    @property
    def has_started(self) -> bool:
        """
        Checks if the match has started.
        This is to be preferred over the 'started' attribute, just in case
        the database update has failed for any reason.
        :return: True if the match has started, False otherwise
        """
        return self.started or self.kickoff_datetime <= datetime.utcnow()

    @property
    def url(self) -> str:
        """
        :return: The URL for this match's info page
        """
        return url_for(
            "info.match",
            league=self.league,
            season=self.season,
            matchday=self.matchday,
            matchup=f"{self.home_team_abbreviation}_"
                    f"{self.away_team_abbreviation}"
        )
