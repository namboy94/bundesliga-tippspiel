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

from flask_login import logout_user
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.ChangePasswordAction import \
    ChangePasswordAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestChangePasswordAction(_ActionTestFramework):
    """
    Class that tests the ChangePassword action
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        generated = self.generate_sample_user(True)
        self.user = generated["user"]  # type: User
        self.pw = generated["pass"]
        self.login_user(self.user)

    def generate_action(self) -> ChangePasswordAction:
        """
        Generates a valid ChangePasswordAction object
        :return: The generated ChangePasswordAction
        """
        return ChangePasswordAction(
            old_password=self.pw,
            new_password="A",
            password_repeat="A"
        )

    def test_using_invalid_password(self):
        """
        Tests using an invalid password
        :return: None
        """
        self.action.old_password = "NoPass"
        with self.context:
            self.failed_execute("Invalid Password")

    def test_mismatching_password(self):
        """
        Tests using a new password that does not match
        with the repeated password
        :return: None
        """
        self.action.password_repeat = "NoPass"
        with self.context:
            self.failed_execute("Password Mismatch")

    def test_successfully_changing_password(self):
        """
        Tests successfully changing the password
        :return: None
        """
        self.assertTrue(self.user.verify_password(self.pw))
        self.assertFalse(self.user.verify_password("A"))
        with self.context:
            self.action.execute()
            self.assertFalse(self.user.verify_password(self.pw))
            self.assertTrue(self.user.verify_password("A"))

    def test_with_unauthorized_user(self):
        """
        Tests that an unauthorized user is correctly identified
        :return: None
        """
        with self.context:
            logout_user()
            self.failed_execute("Unauthorized", 401)
