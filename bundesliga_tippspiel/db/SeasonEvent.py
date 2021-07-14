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
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin


class SeasonEventType(Enum):
    """
    Enumeration that describes all the possible season event types
    """
    PRE_SEASON_MAIL = "pre_season_mail"
    MID_SEASON_REMINDER = "mid_season_reminder"
    POST_SEASON_WRAPUP = "post_season_wrapup"


class SeasonEvent(ModelMixin, db.Model):
    """
    Model that describes the 'season_events' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "season_events"

    season: int = db.Column(db.Integer, primary_key=True)
    league: int = db.Column(db.String(255), primary_key=True)
    event_type: SeasonEventType = db.Column(
        db.Enum(SeasonEventType),
        primary_key=True
    )

    executed: bool = db.Column(db.Boolean, nullable=False, default=False)
