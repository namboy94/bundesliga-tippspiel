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

from unittest import mock
from typing import List, Optional, Tuple
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework
from bundesliga_tippspiel.utils.db import username_exists
from bundesliga_tippspiel.config import smtp_address


class TestRegisterRoute(_RouteTestFramework):
    """
    Class that tests the /register route
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
        return "/register", ["POST"], "Registrierung", False

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.assertFalse(username_exists("TestUser"))

        with mock.patch(
                "bundesliga_tippspiel.actions.RegisterAction.send_email",
                lambda x, y, z: self.assertEqual(x, smtp_address)
        ):
            post = self.client.post("/register", follow_redirects=True, data={
                "username": "TestUser",
                "email": smtp_address,
                "password": "Abc",
                "password-repeat": "Abc",
                "g-recaptcha-response": ""
            })
        self.assertEqual(post.status_code, 200)
        self.assertTrue(b"Siehe in deiner Email-Inbox nach" in post.data)
        self.assertTrue(username_exists("TestUser"))

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.assertFalse(username_exists("TestUser"))
        failed_post = self.client.post(
            "/register",
            follow_redirects=True,
            data={
                "username": "TestUser",
                "email": smtp_address,
                "password": "Abc",
                "password-repeat": "Def",
                "g-recaptcha-response": ""
            }
        )
        self.assertFalse(b"Siehe in deiner Email-Inbox" in failed_post.data)
        self.assertTrue(b"Die angegebenen Passw" in failed_post.data)
        self.assertFalse(username_exists("TestUser2"))
