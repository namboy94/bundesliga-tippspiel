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

import time
import bundesliga_tippspiel.config as config
from unittest import mock
from typing import Tuple, List
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestRegisterApiRoute(_ApiRouteTestFramework):
    """
    Tests the /register API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/update_match_data", ["GET"], False

    def test_content_type(self):
        """
        Tests that an incorrect content type in the request
        is successfully handled
        :return: None
        """
        with mock.patch(
                "bundesliga_tippspiel.routes.api.update.update_db_data"
        ):
            super().test_content_type()

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        with mock.patch(
                "bundesliga_tippspiel.routes.api.update.update_db_data"
        ) as mocked:
            resp = self.client.get(self.route_path)
            self.assertTrue(self.decode_data(resp)["data"]["updated"])
            self.assertEqual(1, mocked.call_count)

            resp = self.client.get(self.route_path)
            self.assertFalse(self.decode_data(resp)["data"]["updated"])
            self.assertEqual(1, mocked.call_count)

            config.last_match_data_update = time.time() - 120

            resp = self.client.get(self.route_path)
            self.assertTrue(self.decode_data(resp)["data"]["updated"])
            self.assertEqual(2, mocked.call_count)

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        pass
