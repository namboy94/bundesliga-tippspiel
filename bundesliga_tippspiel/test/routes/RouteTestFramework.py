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


class _RouteTestFramework(_TestFramework):
    """
    Framework for testing routes
    """

    @property
    def route_info(self) -> Tuple[str, List[str], Optional[str]]:
        """
        Info about the route to test
        :return: The route's path,
                 the route's primary methods,
                 A phrase found on the route's GET page.
                 None if no such page exists
        """
        raise NotImplementedError()

    def test_static(self):
        """
        Tests fetching a static page using GET
        :return: None
        """
        phrase = self.route_info[2]
        if phrase is not None:
            static = self.client.get(self.route_info[0], follow_redirects=True)
            self.assertTrue(bytes(phrase, "utf-8") in static.data)

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
        for method in self.route_info[1]:
            if method == "POST":
                malformed = self.client.post(
                    self.route_info[0],
                    follow_redirects=True,
                    data={}
                )
            elif method == "GET":
                malformed = self.client.get(
                    "{}?alolo=1".format(self.route_info[0]),
                    follow_redirects=True
                )
            else:
                continue

            self.assertEqual(malformed.status_code, 400)
