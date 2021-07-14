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

from flask import url_for
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.db.match_data.Match import Match
if TYPE_CHECKING:  # pragma: no cover
    from bundesliga_tippspiel.db.match_data.Player import Player


class Team(ModelMixin, db.Model):
    """
    Model that describes the 'teams' SQL table
    A Team is the most basic data for a match, it relies on no other data,
    only primitives
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "teams"

    abbreviation: str = db.Column(db.String(3), primary_key=True)
    name: str = db.Column(db.String(50), nullable=False, unique=True)
    short_name: str = db.Column(db.String(16), nullable=False, unique=True)
    icon_svg: str = db.Column(db.String(255), nullable=False)
    icon_png: str = db.Column(db.String(255), nullable=False)

    players: List["Player"] = db.relationship("Player", cascade="all, delete")

    @property
    def home_matches(self) -> List[Match]:
        """
        :return: A list of home matches for the team
        """
        return Match.query.filter_by(
            home_team_abbreviation=self.abbreviation
        ).all()

    @property
    def away_matches(self) -> List[Match]:
        """
        :return: A list of away matches for the team
        """
        return Match.query.filter_by(
            away_team_abbreviation=self.abbreviation
        ).all()

    @property
    def matches(self) -> List[Match]:
        """
        :return: A list of matches for the team
        """
        return self.home_matches + self.away_matches

    @property
    def url(self) -> str:
        """
        :return: The URL for this teams's info page
        """
        return url_for("info.team", team_abbreviation=self.abbreviation)

    @classmethod
    def get_teams_for_season(cls, league: str, season: int) -> List["Team"]:
        """
        Retrieves a list of all teams in a particular season
        :param league: The league in which to search for teams
        :param season: The season in which to search for teams
        :return: The list of teams
        """

        match_samples = Match.query.filter_by(
            league=league, season=season, matchday=1
        ).all()
        home_teams = [x.home_team for x in match_samples]
        away_teams = [x.away_team for x in match_samples]
        return home_teams + away_teams
