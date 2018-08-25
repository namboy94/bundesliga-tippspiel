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
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.utils.db import user_exists, username_exists, \
    email_exists


class TestDb(_TestFramework):
    """
    Class that tests database helper functions
    """

    def test_user_exists_functions(self):
        """
        Tests functions that check if a user exists or not
        :return: None
        """
        existing = self.generate_sample_users()[0]["user"]  # type: User
        not_existing = User(id=3, username="NA", email="na@na.com")

        self.assertTrue(user_exists(existing.id))
        self.assertTrue(email_exists(existing.email))
        self.assertTrue(username_exists(existing.username))

        self.assertFalse(user_exists(not_existing.id))
        self.assertFalse(email_exists(not_existing.email))
        self.assertFalse(username_exists(not_existing.username))
