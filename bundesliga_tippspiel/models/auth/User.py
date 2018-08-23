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


class User(db.Model):
    """
    Model that describes the 'users' SQL table
    A User stores a user's information, including their email address, username
    and password hash
    """

    __tablename__ = "users"
    """
    The name of the table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
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

    def is_authenticated(self) -> bool:
        """
        Method required by flask-login
        :return: True if the user is confirmed, False otherwise
        """
        return self.confirmed

    def is_anonymous(self) -> bool:
        """
        Method required by flask-login
        :return: True if the user is not confirmed, False otherwise
        """
        return not self.is_authenticated()

    # noinspection PyMethodMayBeStatic
    def is_active(self) -> bool:
        """
        Method required by flask-login
        :return: True
        """
        return True

    def get_id(self) -> str:
        """
        Method required by flask-login
        :return: The user's ID as a unicode string
        """
        return str(self.id)
