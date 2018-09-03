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
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException


class ApiKeyDeleteAction(Action):
    """
    Action that allows a user to delete an API key
    """

    def __init__(self, api_key: str):
        """
        Initializes the ApiKeyDeleteAction object
        :param api_key: The API key to delete
        :raises: ActionException if any problems occur
        """
        self.api_key = str(api_key)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        api_key = ApiKey.query.get(self.api_key.split(":", 1)[0])
        if api_key is None:
            raise ActionException(
                "API Key does not exist",
                "Der API Schlüssel existiert nicht"
            )
        elif not api_key.verify_key(self.api_key):
            raise ActionException(
                "API key not valid",
                "Der API Schlüssel ist ungültig"
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        api_key = ApiKey.query.get(self.api_key.split(":", 1)[0])
        db.session.delete(api_key)
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
            data["api_key"]
        )
