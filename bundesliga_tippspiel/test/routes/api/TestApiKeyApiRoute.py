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
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestApiKeyApiRoute(_ApiRouteTestFramework):
    """
    Tests the /api_key API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/api_key", ["POST", "DELETE"], False

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        user = self.generate_sample_user(True)
        generated = self.client.post(self.route_info[0], json={
            "username": user["user"].username,
            "password": user["pass"]
        })
        generated = self.decode_data(generated)
        self.assertTrue("api_key" in generated["data"])
        self.assertTrue("expiration" in generated["data"])

        api_key = generated["data"]["api_key"]
        api_key_obj = ApiKey.query.get(api_key.split(":", 1)[0])
        self.assertIsNotNone(api_key_obj)

        deleted = self.client.delete(self.route_info[0], json={
            "api_key": api_key
        })
        deleted = self.decode_data(deleted)
        self.assertEqual({}, deleted["data"])

        api_key_obj = ApiKey.query.get(api_key.split(":", 1)[0])
        self.assertIsNone(api_key_obj)

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        generated = self.client.post(self.route_info[0], json={
            "username": "A",
            "password": "B"
        })
        self.assertEqual(generated.status_code, 400)
        generated = self.decode_data(generated)
        self.assertEqual(generated["status"], "error")
        self.assertEqual(generated["reason"], "User does not exist")

        deleted = self.client.delete(self.route_info[0], json={
            "api_key": "A"
        })
        self.assertEqual(deleted.status_code, 400)
        deleted = self.decode_data(deleted)
        self.assertEqual(deleted["status"], "error")
        self.assertEqual(deleted["reason"], "API Key does not exist")
