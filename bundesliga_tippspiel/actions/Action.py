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
from flask import abort, redirect, url_for, request
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.types.exceptions import ActionException


class Action:
    """
    A framework class for actions that can be used by normal site requests
    as well as API calls to achieve stuff™.
    """

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        raise NotImplementedError()  # pragma: no cover

    def _execute(self) -> Dict[str, Any]:
        """
        Executes the actual action
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        raise NotImplementedError()  # pragma: no cover

    def execute(self) -> Dict[str, Any]:
        """
        Executes the action after validating user-provided data
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        self.validate_data()
        return self._execute()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def from_site_request(cls):
        """
        Generates an Action object from a site request
        :return: The generated Action object
        """
        try:

            if request.method == "GET":
                data = request.args
            elif request.method == "POST":
                data = request.form
            else:  # pragma: no cover
                raise KeyError()
            return cls.from_dict(data)

        except (KeyError, TypeError, ValueError):
            abort(400)

    def execute_with_redirects(
            self,
            success_url: str,
            success_msg: ActionException,
            failure_url: str
    ) -> str:
        """
        Executes the action and subsequently redirects accordingly
        :param success_url: The URL to which to redirect upon success
        :param success_msg: The message to flash on success
        :param failure_url: The URl to which to redirect upon failure
        :return: The redirect
        """
        try:
            self.execute()

            if isinstance(success_msg, str):
                success_msg = ActionException(
                    success_msg, success_msg, 200, AlertSeverity.SUCCESS
                )

            success_msg.flash()
            return redirect(url_for(success_url))

        except ActionException as e:
            e.flash()
            return redirect(url_for(failure_url))
