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
from flask_login import current_user, logout_user
from bundesliga_tippspiel import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException


class DeleteUserAction(Action):
    """
    Action that allows a user to delete their account
    """

    def __init__(self, password: str):
        """
        Initializes the DeleteUserAction object
        :param password: The password of the user for verification purposes
        :raises: ActionException if any problems occur
        """
        self.password = str(password)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not current_user.is_authenticated:
            raise ActionException(
                "Unauthorized",
                "Du musst hierfür angemeldet sein",
                401
            )
        elif not current_user.verify_password(self.password):
            raise ActionException(
                "Invalid Password",
                "Das angegebene Passwort ist inkorrekt."
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(data["password"])
