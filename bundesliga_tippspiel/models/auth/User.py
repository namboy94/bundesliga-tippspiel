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
from bundesliga_tippspiel.utils.crypto import verify_password


class User(ModelMixin, db.Model):
    """
    Model that describes the 'users' SQL table
    A User stores a user's information, including their email address, username
    and password hash
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "users"
    """
    The name of the table
    """

    username = db.Column(db.String(12), nullable=False, unique=True)
    """
    The user's username
    """

    email = db.Column(db.String(150), nullable=False, unique=True)
    """
    The user's email address
    """

    password_hash = db.Column(db.String(255), nullable=False)
    """
    The user's hashed password, salted and hashed.
    """

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    """
    The account's confirmation status. Logins should be impossible as long as
    this value is False.
    """

    confirmation_hash = db.Column(db.String(255), nullable=False)
    """
    The account's confirmation hash. This is the hash of a key emailed to
    the user. Only once the user follows the link in the email containing the
    key will their account be activated
    """

    @property
    def is_authenticated(self) -> bool:
        """
        Property required by flask-login
        :return: True if the user is confirmed, False otherwise
        """
        return True

    @property
    def is_anonymous(self) -> bool:
        """
        Property required by flask-login
        :return: True if the user is not confirmed, False otherwise
        """
        return not self.is_authenticated  # pragma: no cover

    @property
    def is_active(self) -> bool:
        """
        Property required by flask-login
        :return: True
        """
        return self.confirmed

    def get_id(self) -> str:
        """
        Method required by flask-login
        :return: The user's ID as a unicode string
        """
        return str(self.id)

    def verify_password(self, password: str) -> bool:
        """
        Verifies a password against the password hash
        :param password: The password to check
        :return: True if the password matches, False otherwise
        """
        return verify_password(password, self.password_hash)

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "confirmed": self.confirmed
        }
        if include_children:
            pass
        return data
