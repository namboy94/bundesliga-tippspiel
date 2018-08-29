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
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestAuthorizeApiRoute(_ApiRouteTestFramework):
    """
    Tests the /authorize API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str]]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods
        """
        return "/api/v2/authorize", ["GET"]

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        self.generate_sample_api_key(self.generate_sample_user(True)["user"])

        resp = self.client.get(
            self.route_info[0],
            headers=self.generate_headers("1:{}".format(self.API_KEY))
        )
        self.assertEqual(resp.status_code, 200)
        data = self.decode_data(resp)
        self.assertEqual(data["status"], "ok")

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        resp = self.client.get(
            self.route_info[0],
            headers=self.generate_headers("1:{}".format(self.API_KEY))
        )
        self.assertEqual(resp.status_code, 401)
        data = self.decode_data(resp)
        self.assertEqual(data["status"], "error")
