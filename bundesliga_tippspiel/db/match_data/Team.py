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
if TYPE_CHECKING:  # pragma: no cover
    from bundesliga_tippspiel.db.match_data.Player import Player
    # from bundesliga_tippspiel.db.match_data.Match import Match
    from bundesliga_tippspiel.db.user_generated.SeasonTeamBet import \
        SeasonTeamBet
    from bundesliga_tippspiel.db.user_generated.SeasonPositionBet import \
        SeasonPositionBet


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
    """
    The name of the table
    """

    name: str = db.Column(db.String(50), nullable=False, unique=True)
    """
    The full name of the team. Has to be unique.
    Example: FC Bayern München
    """

    short_name: str = db.Column(db.String(16), nullable=False, unique=True)
    """
    The shortened version of the team's name. Has to be unique.
    Example: Bayern
    """

    abbreviation: str = db.Column(db.String(3), nullable=False, unique=True)
    """
    A three-letter abbreviation of the team's name. Has to be unique.
    Example: FCB
    """

    icon_svg: str = db.Column(db.String(255), nullable=False)
    """
    The URL of an image file representing the team's logo in SVG format
    """

    icon_png: str = db.Column(db.String(255), nullable=False)
    """
    The URL of an image file representing the team's logo in PNG format
    """

    # TODO Figure out how to fix this
    # home_matches: List["Match"] = db.relationship(
    #     "Match", back_populates="home_team", cascade="all, delete"
    # )
    # """
    # The home matches this team plays in.
    # """
    #
    # away_matches: List["Match"] = db.relationship(
    #     "Match", back_populates="away_team", cascade="all, delete"
    # )
    # """
    # The away matches this team plays in.
    # """

    players: List["Player"] = db.relationship(
        "Player", back_populates="team", cascade="all, delete"
    )
    """
    The players of this team
    """

    season_position_bets: List["SeasonPositionBet"] = db.relationship(
        "SeasonPositionBet", back_populates="team", cascade="all, delete"
    )
    """
    The players of this team
    """

    season_team_bets: List["SeasonTeamBet"] = db.relationship(
        "SeasonTeamBet", back_populates="team", cascade="all, delete"
    )
    """
    The players of this team
    """
