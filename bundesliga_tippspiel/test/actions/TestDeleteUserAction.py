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

from flask_login import current_user, logout_user
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.DeleteUserAction import DeleteUserAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestDeleteUserAction(_ActionTestFramework):
    """
    Class that tests the DeleteUser action
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

    def generate_action(self) -> DeleteUserAction:
        """
        Generates a valid DeleteUserAction object
        :return: The generated DeleteUserAction
        """
        return DeleteUserAction(password=self.pw)

    def test_deleting_user(self):
        """
        Tests deleting a user
        :return: None
        """
        with self.context:
            self.assertTrue(current_user.is_authenticated)
            self.assertIsNotNone(User.query.get(self.user.id))
            self.action.execute()
            self.assertFalse(current_user.is_authenticated)
            self.assertIsNone(User.query.get(self.user.id))

    def test_using_wrong_password(self):
        """
        Tests using an incorrect password for verification
        :return: None
        """
        self.action.password = "AAAAA"
        with self.context:
            self.failed_execute("Invalid Password")

    def test_with_unauthorized_user(self):
        """
        Tests that an unauthorized user is correctly identified
        :return: None
        """
        with self.context:
            logout_user()
            self.failed_execute("Unauthorized", 401)
