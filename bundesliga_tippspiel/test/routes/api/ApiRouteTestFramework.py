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
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class _ApiRouteTestFramework(_TestFramework):
    """
    Framework for testing API routes
    """

    @property
    def route_info(self) -> Tuple[str, List[str]]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods
        """
        raise NotImplementedError()

    def test_content_type(self):
        """
        Tests that an incorrect content type in the request
        is successfully handled
        :return: None
        """
        for method in self.route_info[1]:
            if method not in ["POST", "PUT"]:
                continue

            for data, content_type in [
                ({}, "text/html"),
                (None, "application/json"),
                ("", "application/json")
            ]:
                if method == "POST":
                    resp = self.client.post(
                        self.route_info[0],
                        json=data,
                        content_type=content_type
                    )
                else:  # == PUT
                    resp = self.client.put(
                        self.route_info[0],
                        json=data,
                        content_type=content_type
                    )

                self.assertEqual(resp.status_code, 400)
                resp = json.loads(resp.data)
                self.assertEqual(resp["status"], "error")
                self.assertEqual(resp["reason"], "Not in JSON format")

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        raise NotImplementedError()

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        raise NotImplementedError()
