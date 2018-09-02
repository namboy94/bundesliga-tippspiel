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
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.utils.crypto import generate_hash


class ChangePasswordAction(Action):
    """
    Action that allows a user to change their password
    """

    def __init__(
            self, old_password: str, new_password: str, password_repeat: str
    ):
        """
        Initializes the ChangePasswordAction object
        :param old_password: The old password for verification purposes
        :param new_password: The new password
        :param password_repeat: The new password repeated
        :raises: ActionException if any problems occur
        """
        self.old_password = str(old_password)
        self.new_password = str(new_password)
        self.password_repeat = str(password_repeat)

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
        elif not current_user.verify_password(self.old_password):
            raise ActionException(
                "Invalid Password",
                "Das angegebene Passwort ist nicht korrekt"
            )
        elif self.new_password != self.password_repeat:
            raise ActionException(
                "Password Mismatch",
                "Die angegebenen Passwörter stimmen nicht miteinander überein."
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        current_user.password_hash = \
            generate_hash(self.new_password).decode("utf-8")
        db.session.commit()
        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            data["old_password"],
            data["new_password"],
            data["password_repeat"]
        )
