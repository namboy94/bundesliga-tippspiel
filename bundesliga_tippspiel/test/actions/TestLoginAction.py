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
from flask_login import current_user, logout_user
from bundesliga_tippspiel.types.enums import AlertSeverity
from bundesliga_tippspiel.actions.LoginAction import LoginAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestLoginAction(_ActionTestFramework):
    """
    Class that tests the Login action
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

    def generate_action(self) -> LoginAction:
        """
        Generates a valid LoginAction object
        :return: The generated LoginAction
        """
        return LoginAction(
            username=self.confirmed_user.username,
            password=self.confirmed_user_pw,
            remember=True
        )

    def test_logging_in_and_logging_out(self):
        """
        Tests logging in and then logging out
        :return: None
        """
        with self.context:
            self.assertFalse(current_user.is_authenticated)
            self.action.execute()
            self.assertTrue(current_user.is_authenticated)
            logout_user()
            self.assertFalse(current_user.is_authenticated)

    def test_invalid_user(self):
        """
        Tests using an invalid user
        :return: None
        """
        with self.context:
            self.action.username = "NewUser"
            self.failed_execute("User does not exist")

    def test_logging_in_twice(self):
        """
        Tests logging in twice
        :return: None
        """
        with self.context:
            self.action.execute()
            self.failed_execute(
                "Already logged in", severity=AlertSeverity.INFO
            )
            self.assertTrue(current_user.is_authenticated)

    def test_logging_in_unconfirmed_user(self):
        """
        Tests logging in an unconfirmed user
        :return: None
        """
        with self.context:
            self.action.username = self.unconfirmed_user.username
            self.action.password = self.unconfirmed_user_pw
            self.failed_execute("Not confirmed")

    def test_wrong_password(self):
        """
        Tests using the wrong password
        :return: None
        """
        with self.context:
            self.action.password = "A"
            self.failed_execute("Invalid Password")
