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

from typing import Tuple, List, Optional
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.models.auth.User import User


class _RouteTestFramework(_TestFramework):
    """
    Framework for testing routes
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        self.user = User(
            username="RouteUser",
            email="route@hk-tippspiel.com",
            password_hash="$2b$12$xwI3.FxhPmL3EeAgJICetO12AzB"
                          "vEdlBY8bQ1HZtcIjULkZg3/Kb2",
            confirmation_hash="",
            confirmed=True
        )
        self.db.session.add(self.user)
        self.db.session.commit()
        self.pw = "route"

    def login(self):
        """
        Logs in self.user
        :return: None
        """
        resp = self.client.post("/login", follow_redirects=True, data={
            "username": self.user.username,
            "password": self.pw
        })
        self.assertTrue(b"Du hast dich erfolgreich angemeldet" in resp.data)

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
        raise NotImplementedError()

    @property
    def route_path(self) -> str:
        """
        :return: The path of the route
        """
        return self.route_info[0]

    @property
    def methods(self) -> List[str]:
        """
        :return: The primary methods of the route
        """
        return self.route_info[1]

    @property
    def phrase(self) -> Optional[str]:
        """
        :return: A phrase contained in the GET request
        """
        return self.route_info[2]

    @property
    def auth_required(self) -> bool:
        """
        :return: If true, this route requires authentication.
        """
        return self.route_info[3]

    def test_static(self):
        """
        Tests fetching a static page using GET
        :return: None
        """
        if self.phrase is not None:

            if self.auth_required:
                unauthorized = self.client.get(
                    self.route_path, follow_redirects=True
                )
                self.assertEqual(unauthorized.status_code, 401)
                self.login()

            static = self.client.get(self.route_path, follow_redirects=True)
            self.assertEqual(static.status_code, 200)
            self.assertTrue(self.phrase.encode("utf-8") in static.data)

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        raise NotImplementedError()

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        raise NotImplementedError()

    def test_malformed_data(self):
        """
        Tests that malformed data in the request is handled appropriately
        :return: None
        """
        if self.auth_required:
            self.login()

        for method in self.methods:
            if method == "POST":
                malformed = self.client.post(
                    self.route_path,
                    follow_redirects=True,
                    data={}
                )
            elif method == "GET":
                malformed = self.client.get(
                    "{}?alolo=1".format(self.route_path),
                    follow_redirects=True
                )
            else:
                continue

            self.assertEqual(malformed.status_code, 400)
