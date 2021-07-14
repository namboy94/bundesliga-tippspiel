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

from jerrycan.db.User import User
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class TestDb(_TestFramework):
    """
    Class that tests database helper functions
    """

    def test_user_exists_functions(self):
        """
        Tests functions that check if a user exists or not
        :return: None
        """
        existing = self.generate_sample_user()[0]
        not_existing = User(id=3, username="NA", email="na@na.com")

        users = User.query.all()
        user_ids = [x.id for x in users]
        emails = [x.email for x in users]
        usernames = [x.username for x in users]

        self.assertTrue(existing.id in user_ids)
        self.assertTrue(existing.email in emails)
        self.assertTrue(existing.username in usernames)
        self.assertFalse(not_existing.id in user_ids)
        self.assertFalse(not_existing.email in emails)
        self.assertFalse(not_existing.username in usernames)
