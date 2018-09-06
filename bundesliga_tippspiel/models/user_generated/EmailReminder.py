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
from datetime import timedelta
from bundesliga_tippspiel import db
from bundesliga_tippspiel.models.ModelMixin import ModelMixin


class EmailReminder(ModelMixin, db.Model):
    """
    Model that describes the 'email_reminders' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "email_reminders"
    """
    The name of the table
    """

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            "users.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )
    """
    The ID of the user associated with this email reminder
    """

    user = db.relationship(
        "User",
        backref=db.backref("email_reminders", lazy=True, cascade="all,delete")
    )
    """
    The user associated with this email reminder
    """

    before_time = db.Column(db.Integer, nullable=False)
    """
    The time before the next unbet match when the reminder email
    will be sent.
    Unit: seconds
    """

    last_match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    """
    The ID of the last match the user was reminded of
    """

    last_match = db.relationship(
        "Match",
        backref=db.backref("email_reminders", lazy=True, cascade="all,delete")
    )
    """
    The last match he user was reminded of
    """

    @property
    def before_time_delta(self) -> timedelta:
        """
        :return: The 'before_time' parameters as a datetime timedelta
        """
        return timedelta(seconds=self.before_time)

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "last_match_id": self.last_match_id
        }
        if include_children:
            data["user"] = self.user.__json__(True)
            data["last_match"] = self.last_match.__json__(True)
        return data
