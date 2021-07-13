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

from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
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
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("home_team_abbreviation", "away_team_abbreviation",
             "league", "season", "matchday"),
            (Match.home_team_abbreviation, Match.away_team_abbreviation,
             Match.league, Match.season, Match.matchday)
        ),
        db.ForeignKeyConstraint(
            ("player_name", "player_team_abbreviation"),
            (Player.name, Player.team_abbreviation)
        )
    )

    league: str = db.Column(db.String(255), primary_key=True)
    season: int = db.Column(db.Integer, primary_key=True)
    matchday: int = db.Column(db.Integer, primary_key=True)
    home_team_abbreviation: str = db.Column(db.String(3), primary_key=True)
    away_team_abbreviation: str = db.Column(db.String(3), primary_key=True)
    home_score: int = db.Column(db.Integer, primary_key=True)
    away_score: int = db.Column(db.Integer, primary_key=True)

    player_name: str = db.Column(db.String(255), nullable=False)
    player_team_abbreviation: str = db.Column(db.String(3), nullable=False)

    minute: int = db.Column(db.Integer, nullable=False)
    minute_et: int = db.Column(db.Integer, nullable=True, default=0)
    own_goal: bool = db.Column(db.Boolean, nullable=False, default=False)
    penalty: bool = db.Column(db.Boolean, nullable=False, default=False)

    match: Match = db.relationship("Match", overlaps="goals")
    player: Player = db.relationship("Player", overlaps="goals")
