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

import time
from bundesliga_tippspiel import db
from bundesliga_tippspiel.utils.crypto import verify_password


class ApiKey(db.Model):
    """
    Model that describes the 'api_keys' SQL table
    An ApiKey is used for API access using HTTP basic auth
    """

    __tablename__ = "api_keys"
    """
    The name of the table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
    """

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            "users.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the user associated with this API key
    """

    user = db.relationship(
        "User", backref=db.backref("api_keys", lazy=True, cascade="all,delete")
    )
    """
    The user associated with this API key
    """

    key_hash = db.Column(db.String(255), nullable=False)
    """
    The hash of the API key
    """

    creation_time = db.Column(db.Integer, nullable=False)
    """
    The time at which this API key was created as a UNIX timestamp
    """

    def has_expired(self) -> bool:
        """
        Checks if the API key has expired.
        API Keys expire after 30 days
        :return: True if the key has expired, False otherwise
        """
        return time.time() - self.creation_time > 2592000

    def verify_key(self, key: str) -> bool:
        """
        Checks if a given key is valid
        :param key: The key to check
        :return: True if the key is valid, False otherwise
        """
        _id, api_key = key.split(":", 1)
        if _id != self.id:
            return False
        else:
            return verify_password(api_key, self.key_hash)
