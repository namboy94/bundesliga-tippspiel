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
from jerrycan.db.User import User


class DisplayBotsSettings(ModelMixin, db.Model):
    """
    Database model that specifies whether a user wants to see bots or not
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "display_bot_settings"
    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    display_bots = db.Column(db.Boolean, nullable=False, default=True)

    user: User = db.relationship(
        "User",
        backref=db.backref("display_bot_settings", cascade="all, delete")
    )

    @classmethod
    def get_state(cls, user: User):
        """
        Retrieves the state of the settings for a give user
        :param user: The user for which to retrieve the seetings
        :return: True if active, False otherwise
        """
        bot_setting = DisplayBotsSettings.query.filter_by(
            user_id=user.id
        ).first()
        return bot_setting is not None and bot_setting.display_bots

    @staticmethod
    def bot_symbol() -> str:
        """
        :return: "The bot unicode symbol"
        """
        return "🤖"
