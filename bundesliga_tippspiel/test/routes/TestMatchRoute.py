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


class TestMatchRoute(_RouteTestFramework):
    """
    Class that tests the /match route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return:
        """
        super().setUp()
        self.team_one, self.team_two, self.player, self.match, self.goal = \
            self.generate_sample_match_data()
        self.bet = self.generate_sample_bet(self.user, self.match)

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
        return "/match/{}".format(self.match.id), [], "VS", True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        resp = self.client.get(self.route_path).data
        self.assertTrue(self.team_one.short_name.encode("utf-8") in resp)
        self.assertTrue(self.team_two.short_name.encode("utf-8") in resp)
        self.assertTrue(self.goal.player.name.encode("utf-8") in resp)
        self.assertTrue(self.bet.user.username.encode("utf-8") in resp)

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        resp = self.client.get(self.route_path)
        self.assertEqual(resp.status_code, 401)

        self.login()
        resp = self.client.get("/match/1000")
        self.assertEqual(resp.status_code, 404)
