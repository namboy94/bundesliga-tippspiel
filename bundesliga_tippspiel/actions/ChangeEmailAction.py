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
from flask_login import current_user
from bundesliga_tippspiel import db
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.utils.crypto import verify_password


class ChangeEmailAction(Action):
    """
    Action that allows a user to change their email address
    """

    def __init__(self, email: str, password: str):
        """
        Initializes the ChangeEmailAction object
        :param email: The new email address
        :param password: The user's password for verification purposes
        :raises: ActionException if any problems occur
        """
        self.email = email
        self.password = password

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not verify_password(self.password, current_user.password_hash):
            raise ActionException(
                "Invalid Password",
                "Das angegebene Passwort ist nicht korrekt"
            )
        elif len(User.query.filter_by(email=self.email).all()) > 0:
            raise ActionException(
                "Email exists",
                "Diese Email Adresse wird bereits verwendet"
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        current_user.email = self.email
        db.session.commit()
        return {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            data["email"],
            data["password"]
        )
