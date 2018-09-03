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

from typing import Tuple, List
from bundesliga_tippspiel.models.auth.User import User
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestChangePasswordApiRoute(_ApiRouteTestFramework):
    """
    Tests the /change_password API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/change_password", ["POST"], True

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        previous_hash = self.user.password_hash
        resp = self.client.post(
            self.route_path,
            headers=self.generate_headers(),
            json={
                "old_password": self.pw,
                "new_password": self.pw + "AAA",
                "password_repeat": self.pw + "AAA"
            }
        )
        resp_data = self.decode_data(resp)
        self.assertEqual(resp_data["status"], "ok")
        user = User.query.get(self.user.id)
        self.assertNotEqual(previous_hash, user.password_hash)
        self.assertTrue(user.verify_password(self.pw + "AAA"))

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        previous_hash = self.user.password_hash
        resp = self.client.post(
            self.route_path,
            headers=self.generate_headers(),
            json={
                "old_password": self.pw,
                "new_password": self.pw + "AAA",
                "password_repeat": self.pw + "AA"
            }
        )
        resp_data = self.decode_data(resp)
        self.assertEqual(resp_data["status"], "error")
        self.assertEqual(resp_data["reason"], "Password Mismatch")
        self.assertEqual(previous_hash, self.user.password_hash)
        self.assertFalse(self.user.verify_password(self.pw + "AAA"))
