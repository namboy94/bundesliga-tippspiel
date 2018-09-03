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
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.utils.db import user_exists
from bundesliga_tippspiel.utils.crypto import verify_password
from bundesliga_tippspiel.actions.Action import Action


class ConfirmAction(Action):
    """
    Action that allows the confirmation of previously registered users
    """

    def __init__(self, user_id: int, confirm_key: str):
        """
        Initializes the ConfirmAction object
        :param user_id: The user's ID
        :param confirm_key: The user's confirmation key
        :raises: ActionException if any problems occur
        """
        self.user_id = int(user_id)
        self.confirm_key = str(confirm_key)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not user_exists(self.user_id):
            raise ActionException(
                "User does not exist",
                "Dieser Nutzer existiert nicht"
            )
        else:
            user = User.query.get(self.user_id)
            if user.confirmed:
                raise ActionException(
                    "Already Confirmed",
                    "Dieser Nutzer is bereits bestätigt worden.",
                    severity=AlertSeverity.WARNING
                )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        user = User.query.get(self.user_id)
        verified = verify_password(self.confirm_key, user.confirmation_hash)

        if verified:
            user.confirmed = True
            db.session.commit()
        else:
            raise ActionException(
                "Invalid Confirmation Key",
                "Der angegebene Bestätigungsschlüssel ist inkorrekt."
            )
        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            int(data["user_id"]),
            data["confirm_key"]
        )
