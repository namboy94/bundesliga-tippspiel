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

from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.types.exceptions import ActionException
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class _ActionTestFramework(_TestFramework):
    """
    Framework for testing Action classes
    """

    __action = None  # type: Action
    """
    Inner action used by the action property to achieve persistence
    """

    @property
    def action(self) -> Action:
        """
        Retrieves the instance's Action object,
        while not generating one each time
        :return: An Action object that will run successfully upon executing
        """
        if self.__action is None:
            self.__action = self.generate_action()
        return self.__action

    def generate_action(self) -> Action:
        """
        Generates a new, valid Action object
        :return: The generated object
        """
        raise NotImplementedError()

    def failed_execute(
            self,
            error_reason: str,
            error_code: int = 400,
            severity: AlertSeverity = AlertSeverity.DANGER
    ):
        """
        Executes the instance's action object while assuring that it fails,
        raising an ActionException, then verifying that the correct error
        was thrown.
        :param error_reason: The reason for the error
        :param error_code: The error code to check
        :param severity: The severity of the error, defaults to DANGER
        :return: None
        """
        try:
            self.action.execute()
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, error_reason)
            self.assertEqual(e.status_code, error_code)
            self.assertEqual(e.severity, severity)
