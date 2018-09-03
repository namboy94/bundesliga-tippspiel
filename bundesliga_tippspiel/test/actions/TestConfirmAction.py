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

from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.actions.ConfirmAction import ConfirmAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestConfirmAction(_ActionTestFramework):
    """
    Class that tests the Confirm action
    """

    def setUp(self):
        """
        Sets up users for testing
        :return: None
        """
        super().setUp()
        generated_users = self.generate_sample_users()
        self.confirmed_user = generated_users[0]["user"]  # type: User
        self.confirmed_user_pw = generated_users[0]["pass"]
        self.unconfirmed_user = generated_users[1]["user"]  # type: User
        self.unconfirmed_user_pw = generated_users[1]["pass"]

    def generate_action(self) -> ConfirmAction:
        """
        Generates a valid ConfirmAction object
        :return: The generated ConfirmAction
        """
        return ConfirmAction(
            user_id=self.unconfirmed_user.id,
            confirm_key=self.unconfirmed_user_pw
        )

    def test_invalid_user(self):
        """
        Tests using an invalid user
        :return: None
        """
        self.action.user_id = 100
        self.failed_execute("User does not exist")

    def test_confirming_already_confirmed_user(self):
        """
        Tests confirming a user that's already confirmed
        :return: None
        """
        self.action.user_id = self.confirmed_user.id
        self.action.confirm_key = self.confirmed_user_pw
        self.failed_execute(
            "Already Confirmed", severity=AlertSeverity.WARNING
        )

    def test_using_invalid_key(self):
        """
        Tests using an invalid confirmation key
        :return: None
        """
        self.action.confirm_key = "AAA"
        self.failed_execute("Invalid Confirmation Key")

    def test_confirming(self):
        """
        Tests successfully confirming a user
        :return: None
        """
        self.assertFalse(self.unconfirmed_user.confirmed)
        self.action.execute()
        self.assertTrue(self.unconfirmed_user.confirmed)
