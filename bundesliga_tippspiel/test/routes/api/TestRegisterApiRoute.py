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

import json
from typing import Tuple, List
from bundesliga_tippspiel.config import smtp_address
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestRegisterApiRoute(_ApiRouteTestFramework):
    """
    Tests the /register API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str]]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods
        """
        return "/api/v2/register", ["POST"]

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        resp = self.client.post(self.route_info[0], json={
            "username": "TestUser",
            "email": smtp_address,
            "password": "Abc",
            "password-repeat": "Abc",
            "g-recaptcha-response": ""
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data["data"]["user_id"], 1)
        self.assertTrue("confirm_key" in resp_data["data"])

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        resp = self.client.post(self.route_info[0], json={
            "username": "TestUser",
            "email": smtp_address,
            "password": "Abc",
            "password-repeat": "Def",
            "g-recaptcha-response": ""
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data["reason"], "Password Mismatch")
