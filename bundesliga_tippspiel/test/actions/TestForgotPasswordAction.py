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

import time
from bundesliga_tippspiel.utils.email import get_inbox_count
from bundesliga_tippspiel.config import smtp_address
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.utils.crypto import verify_password
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import\
    _ActionTestFramework
from bundesliga_tippspiel.actions.ForgotPasswordAction import \
    ForgotPasswordAction


class TestForgotPasswordAction(_ActionTestFramework):
    """
    Test class that tests the forgot password action
    """

    def setUp(self):
        """
        Sets up a user in the database
        :return: None
        """
        super().setUp()
        user = self.generate_sample_user(True)
        self.user = user["user"]  # type: User
        self.password = user["pass"]
        self.user.email = smtp_address
        self.db.session.commit()

    def generate_action(self) -> ForgotPasswordAction:
        """
        Generates a new, valid Action object
        :return: The generated object
        """
        return ForgotPasswordAction(
            self.user.email, "", "localhost", "localhost"
        )

    @_ActionTestFramework.online_required
    def test_resetting_password(self):
        """
        Tests successfully resetting the password of a user
        :return: None
        """
        self.assertTrue(
            verify_password(self.password, self.user.password_hash)
        )
        before_count = get_inbox_count()
        self.action.execute()
        self.assertFalse(
            verify_password(self.password, self.user.password_hash)
        )
        time.sleep(1)
        self.assertEqual(before_count + 1, get_inbox_count())

    def test_non_existant_email(self):
        """
        Tests resetting the password of an email address that's not registered
        :return: None
        """
        self.action.email = "a@hk-tippspiel.com"
        self.failed_execute("Email not registered")

    @_ActionTestFramework.online_required
    def test_invalid_recaptcha(self):
        """
        Tests using an invalid ReCaptcha response
        :return: None
        """
        self.action.client_address = "1"
        self.failed_execute("Invalid ReCaptcha Response")
