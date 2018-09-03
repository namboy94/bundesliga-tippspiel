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
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.config import smtp_address
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction
from bundesliga_tippspiel.utils.email import get_inbox_count
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestRegisterAction(_ActionTestFramework):
    """
    Tests the RegisterAction class
    """

    def generate_action(self) -> RegisterAction:
        """
        Generates a valid RegisterAction object
        :return: The generated RegisterAction
        """
        return RegisterAction(
            "TestUser", smtp_address, "Abc", "localhost", "localhost", ""
        )

    # noinspection PyUnresolvedReferences
    @_ActionTestFramework.online_required
    def test_registering(self):
        """
        Tests registering a new user
        :return: None
        """
        emails_before = get_inbox_count()
        self.assertEqual(
            len(User.query.filter_by(username=self.action.username).all()), 0
        )
        self.action.execute()
        time.sleep(1)
        self.assertEqual(
            len(User.query.filter_by(username=self.action.username).all()), 1
        )
        emails_after = get_inbox_count()
        self.assertEqual(emails_before + 1, emails_after)

    def test_too_long_username(self):
        """
        Tests using a username that's too long
        :return: None
        """
        self.action.username = "A" * 13
        self.failed_execute("Username too long")

    def test_too_short_username(self):
        """
        Tests using a username that's too short
        :return: None
        """
        self.action.username = ""
        self.failed_execute("Username too short")

    def test_username_with_colon(self):
        """
        Tests using a username containing a colon
        :return: None
        """
        self.action.username = "A:B"
        self.failed_execute("Username contains colon")

    def test_mismatching_passwords(self):
        """
        Tests using passwords that don't match
        :return: None
        """
        # noinspection PyUnresolvedReferences
        self.action.password_repeat = self.action.password.upper()
        self.failed_execute("Password Mismatch")

    def test_existing_username(self):
        """
        Tests using a username that already exists
        :return: None
        """
        one = self.generate_sample_users()[0]["user"]  # type: User
        self.action.username = one.username
        self.failed_execute("Username already exists")

    def test_existing_email(self):
        """
        Tests using an email address that already exists
        :return: None
        """
        one = self.generate_sample_users()[0]["user"]  # type: User
        self.action.email = one.email
        self.failed_execute("Email already exists")

    @_ActionTestFramework.online_required
    def test_invalid_recaptcha(self):
        """
        Tests using an invalid recaptcha response
        :return: None
        """
        self.action.client_address = "1"
        self.failed_execute("Invalid ReCaptcha Response")
