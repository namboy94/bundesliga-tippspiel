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

from bundesliga_tippspiel.test.TestFramework import TestFramework,\
    online_required
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.register import register
from bundesliga_tippspiel.config import smtp_address
from bundesliga_tippspiel.exceptions import ActionException


class TestRegister(TestFramework):
    """
    Tests the 'register' action
    """

    @online_required
    def test_registering(self):
        """
        Tests registering a new user
        :return: None
        """
        self.assertEqual(
            len(User.query.filter_by(username="TestUser").all()), 0
        )
        register("TestUser", smtp_address, "pass", "localhost", "")
        self.assertEqual(
            len(User.query.filter_by(username="TestUser").all()), 1
        )

    def test_too_long_username(self):
        """
        Tests using a username that's too long
        :return: None
        """
        try:
            register("T" * 13, smtp_address, "pass", "localhost", "")
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "Username too long")

    def test_too_short_username(self):
        """
        Tests using a username that's too short
        :return: None
        """
        try:
            register("", smtp_address, "pass", "localhost", "")
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "Username too short")

    def test_existing_username(self):
        """
        Tests using a username that already exists
        :return: None
        """
        one = self.generate_sample_users()[0]["user"]  # type: User
        try:
            register(one.username, smtp_address, "pass", "localhost", "")
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "Username already exists")

    def test_existing_email(self):
        """
        Tests using an email address that already exists
        :return: None
        """
        one = self.generate_sample_users()[0]["user"]  # type: User
        try:
            register("TestUser", one.email, "pass", "localhost", "")
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "Email already exists")

    @online_required
    def test_invalid_recaptcha(self):
        """
        Tests using an invalid recaptcha response
        :return: None
        """
        try:
            register("TestUser", smtp_address, "pass", "1", "AAA")
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "Invalid ReCaptcha Response")
