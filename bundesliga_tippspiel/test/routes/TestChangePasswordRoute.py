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


class TestChangePasswordRoute(_RouteTestFramework):
    """
    Class that tests the /change_password route
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
        return "/change_password", ["POST"], None, True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        previous_hash = self.user.password_hash
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            "old_password": self.pw,
            "new_password": self.pw + "AAA",
            "password_repeat": self.pw + "AAA"
        })
        self.assertTrue(b"Dein Passwort wurde erfolgreich ge" in resp.data)
        self.assertNotEqual(previous_hash, self.user.password_hash)
        self.assertTrue(self.user.verify_password(self.pw + "AAA"))

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.login()
        previous_hash = self.user.password_hash
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            "old_password": self.pw,
            "new_password": self.pw + "AAA",
            "password_repeat": self.pw + "A"
        })
        self.assertFalse(b"Dein Passwort wurde erfolgreich ge" in resp.data)
        self.assertTrue(b"stimmen nicht miteinander" in resp.data)
        self.assertEqual(previous_hash, self.user.password_hash)
        self.assertFalse(self.user.verify_password(self.pw + "AAA"))
