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

from flask import request
from flask_login import login_user, current_user
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.utils.db import username_exists
from bundesliga_tippspiel.utils.crypto import verify_password
from bundesliga_tippspiel.actions.Action import Action


class LoginAction(Action):
    """
    Action that allows the logging in of users
    """

    def __init__(self, username: str, password: str, remember: bool):
        """
        Initializes the LoginAction object
        :param username: The user's username
        :param password: The user's password
        :param remember: If set to true, the login session will be persistent
        :raises: ActionException if any problems occur
        """
        self.username = username
        self.password = password
        self.remember = remember

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not username_exists(self.username):
            raise ActionException(
                "User does not exist",
                "Dieser User ist nicht registriert"
            )
        elif current_user.is_authenticated:
            raise ActionException(
                "Already logged in",
                "Du bist bereits angemeldet.",
                AlertSeverity.INFO
            )
        else:
            user = User.query.filter_by(username=self.username).first()
            if not user.confirmed:
                raise ActionException(
                    "Not confirmed",
                    "Dieser Nutzer wurde noch nicht bestätigt"
                )

    def _execute(self):
        """
        Logins a previously registered user
        :return: None
        :raises ActionException: if anything went wrong
        """
        user = User.query.filter_by(username=self.username).first()
        verified = verify_password(self.password, user.password_hash)

        if verified:
            login_user(user, remember=self.remember)
        else:
            raise ActionException(
                "Invalid Password",
                "Das angegebene Password ist inkorrekt."
            )

    @classmethod
    def _from_site_request(cls) -> Action:
        """
        Generates a LoginAction object from a site request
        :return: The generated LoginAction object
        """
        return cls(
            request.form["username"],
            request.form["password"],
            request.form.get("remember_me") == "on"
        )
