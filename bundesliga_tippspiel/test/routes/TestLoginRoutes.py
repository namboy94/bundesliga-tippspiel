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
from bundesliga_tippspiel.test.TestFramework import TestFramework


class TestLoginRoutes(TestFramework):
    """
    Class that tests the routes defined by registration routes
    """

    def test_logging_in(self):
        """
        Tests the /login route
        :return: None
        """
        userdata = self.generate_sample_users()[0]
        user, password = userdata["user"], userdata["pass"]

        page = self.client.get("/login")
        self.assertTrue(b"Anmelden" in page.data)

        success = self.client.post("/login", follow_redirects=True, data={
            "username": user.username,
            "password": password
        })
        self.assertTrue(b"Du hast dich erfolgreich angemeldet" in success.data)

        self.client.get("/logout")

        failure = self.client.post("/login", follow_redirects=True, data={
            "username": user.username,
            "password": "ABC"
        })
        self.assertFalse(
            b"Du hast dich erfolgreich angemeldet" in failure.data
        )
        self.assertTrue(
            b"Das angegebene Password ist inkorrekt" in failure.data
        )

        malformed = self.client.post("/login", follow_redirects=True, data={})
        self.assertEqual(400, malformed.status_code)
