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
from bundesliga_tippspiel import db
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
        :raises: ActionException if any problems occur
        """
        self.user_id = user_id
        self.confirm_key = confirm_key

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not user_exists(self.user_id):
            raise ActionException(
                "User does not exist",
                "Dieser Username existiert nicht"
            )

    def _execute(self):
        """
        Confirms a previously registered user
        :return: None
        :raises ActionException: if anything went wrong
        """
        user = User.query.filter_by(id=self.user_id).first()
        verified = verify_password(self.confirm_key, user.confirmation_hash)

        if verified:
            user.confirmed = True
            db.session.commit()
        else:
            raise ActionException(
                "Invalid Confirmation",
                "Der angegebene Bestätigungsschlüssel ist inkorrekt."
            )

    @classmethod
    def _from_site_request(cls) -> Action:
        """
        Generates a ConfirmAction object from a site request
        :return: The generated ConfirmAction object
        """
        return cls(
            int(request.args["user"]),
            request.args["confirm_key"]
        )
