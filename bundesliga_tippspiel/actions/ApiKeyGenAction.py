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
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.utils.crypto import verify_password, generate_hash, \
    generate_random


class ApiKeyGenAction(Action):
    """
    Action that allows a user to generate a new API key
    """

    def __init__(self, username: str, password: str):
        """
        Initializes the ApiKeyGenAction object
        :param username: The user's username
        :param password: The user's password
        :raises: ActionException if any problems occur
        """
        self.username = str(username)
        self.password = str(password)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        user = User.query.filter_by(username=self.username).first()
        if user is None:
            raise ActionException(
                "User does not exist",
                "Der spezifizierte Nutzer existiert nicht"
            )
        elif not user.confirmed:
            raise ActionException(
                "User is not confirmed",
                "Der spezifizierte Nutzer wurde noch nicht bestätigt"
            )
        elif not verify_password(self.password, user.password_hash):
            raise ActionException(
                "Invalid Password",
                "Das angegebene Passwort ist nicht korrekt"
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        user = User.query.filter_by(username=self.username).first()

        key = generate_random(20)
        hashed = generate_hash(key).decode("utf-8")
        api_key = ApiKey(user=user, key_hash=hashed)

        db.session.add(api_key)
        db.session.commit()

        return {
            "api_key": "{}:{}".format(api_key.id, key.decode("utf-8")),
            "expiration": int(api_key.creation_time) + ApiKey.MAX_AGE
        }

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            data["username"],
            data["password"]
        )
