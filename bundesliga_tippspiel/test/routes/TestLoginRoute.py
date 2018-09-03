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

from typing import Tuple, Optional, List
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestLoginRoute(_RouteTestFramework):
    """
    Class that tests the /login route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], Optional[str], bool]:
        """
        Info about the route to test
        :return: The route's path,
                 the route's primary methods,
                 A phrase found on the route's GET page.
                 None if no such page exists,
                 An indicator for if the page requires authentication or not
        """
        return "/login", ["POST"], "Anmelden", False

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        userdata = self.generate_sample_users()[0]
        user, password = userdata["user"], userdata["pass"]

        success = self.client.post("/login", follow_redirects=True, data={
            "username": user.username,
            "password": password
        })
        self.assertTrue(b"Du hast dich erfolgreich angemeldet" in success.data)

        self.client.get("/logout")

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        failure = self.client.post("/login", follow_redirects=True, data={
            "username": "A",
            "password": "ABC"
        })
        self.assertFalse(
            b"Du hast dich erfolgreich angemeldet" in failure.data
        )
        self.assertTrue(
            b"Dieser User ist nicht registriert" in failure.data
        )
