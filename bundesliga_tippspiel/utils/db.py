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

from bundesliga_tippspiel.models.auth.User import User

"""
A collection of functions to simplify common database operations
"""


def user_exists(user_id: int) -> bool:
    """
    Checks if a username already exists in the database
    :param user_id: The user's id
    :return: True if the user exists, False otherwise
    """
    return len(User.query.filter_by(id=user_id).all()) > 0


def username_exists(username: str) -> bool:
    """
    Checks if a username already exists in the database
    :param username: The username to check
    :return: True if the username exists in the database, False if not
    """
    return len(User.query.filter_by(username=username).all()) > 0


def email_exists(email: str) -> bool:
    """
    Checks if an email address already exists in the database
    :param email: The email to check for
    :return: True if the email exists in the database, False otherwise
    """
    return len(User.query.filter_by(email=email).all()) > 0
