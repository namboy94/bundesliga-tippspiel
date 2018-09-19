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

from typing import Dict, Any, Optional, List
from flask import abort, redirect, url_for, request
from bundesliga_tippspiel import db
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.models.ModelMixin import ModelMixin
from bundesliga_tippspiel.models.match_data.Match import Match


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
        try:
            return cls._from_dict(data)
        except (ValueError, TypeError):
            raise ActionException(
                "invalid parameters",
                "Ungültige Parameter"
            )

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
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

    @staticmethod
    def handle_id_fetch(_id: int, query_cls: type(db.Model)) -> db.Model:
        """
        Handles fetching a single object by using it's ID
        Raises an ActionException if an ID does not exist
        :return: The object identified by the ID
        :raises ActionException: Without fail
        """
        result = query_cls.query.get(_id)
        if result is None:
            raise ActionException(
                "ID does not exist",
                "Die angegebene ID existiert nicht",
                404
            )
        else:
            return result

    @staticmethod
    def check_id_or_filters(
            _id: Optional[int], filters: List[Optional[Any]]
    ):
        """
        Checks that no filters are applied if a specific ID was provided
        :param _id: The specific ID
        :param filters: A list of filters
        :return: None
        """
        has_filter = len(list(filter(lambda x: x is not None, filters))) > 0
        if has_filter and _id is not None:
            raise ActionException(
                "Can't filter specific ID",
                "Eine spezifische ID kann nicht gefiltered werden"
            )

    @staticmethod
    def resolve_and_check_matchday(matchday: Optional[int]) -> Optional[int]:
        """
        Checks the bound of a matchday
        :param matchday: The matchday to check
        :return: None
        :raises ActionException: If the matchday is invalid
        """
        if matchday is not None:
            if matchday == -1:
                all_matches = Match.query.all()
                filtered = list(filter(lambda x: not x.started, all_matches))
                matchday = min(filtered, key=lambda x: x.matchday).matchday
            elif not 0 < matchday < 35:
                raise ActionException(
                    "Matchday out of bounds",
                    "Den angegebenen Spieltag gibt es nicht"
                )
        return matchday

    def prepare_get_response(self, result: List[ModelMixin], keyword: str) \
            -> Dict[str, Any]:
        """
        Prepares a GetAction response by
        :param result: The result to wrap in a response dictionary
        :param keyword: The keyword to use, e.g: bet|match|player etc.
        :return: The wrapped response dictionary
        """
        if keyword in ["match"]:
            response = {"{}es".format(keyword): result}
        else:
            response = {"{}s".format(keyword): result}

        if getattr(self, "id", None) is not None:
            response[keyword] = result[0]

        return response
