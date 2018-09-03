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

    home_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the home team. Acts as a foreign key
    """

    home_team = db.relationship(
        "Team", foreign_keys=[home_team_id], cascade="all,delete"
    )
    """
    The home team.
    """

    away_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the away team. Acts as a foreign key
    """

    away_team = db.relationship(
        "Team", foreign_keys=[away_team_id], cascade="all,delete"
    )
    """
    The away team.
    """

    matchday = db.Column(db.Integer, nullable=False)
    """
    The match day of the match
    """

    home_current_score = db.Column(db.Integer)
    """
    The current score of the home team.
    """

    away_current_score = db.Column(db.Integer)
    """
    The current score of the away team.
    """

    home_ht_score = db.Column(db.Integer)
    """
    The score of the home team at half time
    """

    away_ht_score = db.Column(db.Integer)
    """
    The score of the away team at half time
    """

    home_ft_score = db.Column(db.Integer)
    """
    The final score of the home team
    """

    away_ft_score = db.Column(db.Integer)
    """
    The final score of the away team
    """

    kickoff = db.Column(db.String(255), nullable=False)
    """
    A string representing the kickoff time in UTC in the following format:
    YYYY-MM-DD:HH-mm-ss
    If the kickoff time is not known, it should be set to 'TBD'
    """

    started = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has started yet
    """

    finished = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has finished yet
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
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "matchday": self.matchday,
            "home_current_score": self.home_current_score,
            "away_current_score": self.away_current_score,
            "home_ht_score": self.home_ht_score,
            "away_ht_score": self.away_ht_score,
            "home_ft_score": self.home_ft_score,
            "away_ft_score": self.away_ft_score,
            "kickoff": self.kickoff,
            "started": self.started,
            "finished": self.finished
        }
        if include_children:
            data["home_team"] = self.home_team.__json__(include_children)
            data["away_team"] = self.away_team.__json__(include_children)
        return data
