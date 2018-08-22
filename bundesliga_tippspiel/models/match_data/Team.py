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

from bundesliga_tippspiel import db


class Team(db.Model):
    """
    Model that describes the 'teams' SQL table
    A Team is the most basic data for a match, it relies on no other data,
    only primitives
    """

    __tablename__ = "teams"
    """
    The name of the table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
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
