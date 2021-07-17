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
from typing import Optional

from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.db.User import User
from bundesliga_tippspiel.db import Team


class UserProfile(ModelMixin, db.Model):
    """
    Model that describes the 'user_profiles' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "user_profiles"

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    favourite_team_abbreviation: Optional[str] = db.Column(
        db.String(3),
        db.ForeignKey("teams.abbreviation"),
        nullable=True
    )
    description: Optional[str] = db.Column(db.String(255), nullable=True)
    country: Optional[str] = db.Column(db.String(255), nullable=True)

    user: User = db.relationship(
        "User",
        backref=db.backref("profile", cascade="all, delete", uselist=False),
    )
    favourite_team: Team = db.relationship("Team")
