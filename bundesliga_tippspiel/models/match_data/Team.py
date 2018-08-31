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

    name = db.Column(db.String(50), nullable=False, unique=True)
    """
    The full name of the team. Has to be unique.
    Example: FC Bayern München
    """

    short_name = db.Column(db.String(16), nullable=False, unique=True)
    """
    The shortened version of the team's name. Has to be unique.
    Example: Bayern
    """

    abbreviation = db.Column(db.String(3), nullable=False, unique=True)
    """
    A three-letter abbreviation of the team's name. Has to be unique.
    Example: FCB
    """

    icon_svg = db.Column(db.String(255), nullable=False)
    """
    The URL of an image file representing the team's logo in SVG format
    """

    icon_png = db.Column(db.String(255), nullable=False)
    """
    The URL of an image file representing the team's logo in PNG format
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
            "name": self.name,
            "short_name": self.short_name,
            "abbreviation": self.abbreviation,
            "icon_svg": self.icon_svg,
            "icon_png": self.icon_png
        }
        if include_children:
            pass
        return data
