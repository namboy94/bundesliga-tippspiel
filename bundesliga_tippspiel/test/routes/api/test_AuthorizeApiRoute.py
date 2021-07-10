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
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/authorize", ["GET"], False

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        user = self.generate_sample_user(True)[0]
        api_key = self.generate_api_key(user)[1]
        headers = self.generate_api_key_headers(api_key)

        resp = self.client.get(
            self.route_info[0],
            headers=headers,
            json={}
        )
        self.assertEqual(resp.status_code, 200)
        data = self.decode_data(resp)
        self.assertEqual(data["status"], "ok")

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        headers = self.generate_headers(
            f"{self.api_key_obj.id + 1}:{self.api_key.split(':')[1]}"
        )
        resp = self.client.get(self.route_info[0], headers=headers)
        self.assertEqual(resp.status_code, 401)
        data = self.decode_data(resp)
        self.assertEqual(data["status"], "error")

    def test_expired_api_key(self):
        """
        Tests using an expired API key
        :return: None
        """
        api_key, api_key_value, _ = self.generate_api_key(
            self.generate_sample_user(True)[0]
        )
        api_key.creation_time = 0
        self.db.session.commit()

        resp = self.client.get(
            self.route_info[0],
            headers=self.generate_headers(
                "{}:{}".format(api_key.id, api_key_value)
            )
        )
        self.assertEqual(resp.status_code, 401)
        data = self.decode_data(resp)
        self.assertEqual(data["status"], "error")
