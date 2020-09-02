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
from typing import Dict, Any
from puffotter.flask.base import db
from puffotter.flask.db.ModelMixin import ModelMixin


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
    """
    The name of the table
    """

    event_type: SeasonEventType = db.Column(
        db.Enum(SeasonEventType),
        nullable=False,
        unique=True
    )
    """
    The type of event
    """

    executed: bool = db.Column(db.Boolean, nullable=False, default=False)
    """
    Whether the event was executed or not
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
            "event_type": self.event_type.value,
            "executed": self.executed
        }
        return data
