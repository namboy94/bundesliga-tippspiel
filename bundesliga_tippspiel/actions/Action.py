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

    def _execute(self):
        """
        Executes the actual action
        :return: None
        :raises ActionException: if anything went wrong
        """
        raise NotImplementedError()  # pragma: no cover

    def execute(self):
        """
        Executes the action after validating user-provided data
        :return: None
        :raises ActionException: if anything went wrong
        """
        self.validate_data()
        self._execute()

    @classmethod
    def from_site_request(cls):
        """
        Generates an Action object from a site request
        :return: The generated Action object
        """
        raise NotImplementedError()  # pragma: no cover
