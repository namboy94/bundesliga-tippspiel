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
from bundesliga_tippspiel.models.match_data.Match import Match
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestTeamRoute(_RouteTestFramework):
    """
    Class that tests the /team route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return:
        """
        super().setUp()
        self.team_one, self.team_two, self.player, _, _ = \
            self.generate_sample_match_data()
        self.match_one = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:01",
            started=True, finished=True,
            home_current_score=1, away_current_score=1
        )
        self.match_two = Match(
            home_team=self.team_two, away_team=self.team_one,
            matchday=2, kickoff="2019-01-01:01:02:02",
            started=True, finished=True,
            home_current_score=2, away_current_score=1
        )
        self.match_three = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=3, kickoff="2019-01-01:01:02:03",
            started=True, finished=True,
            home_current_score=2, away_current_score=1
        )
        self.db.session.add(self.match_one)
        self.db.session.add(self.match_two)
        self.db.session.add(self.match_three)
        self.db.session.commit()

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
        return "/team/{}".format(self.team_one.id), \
               [], \
               self.team_one.name, \
               True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        resp = self.client.get(self.route_path)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b"1:1" in resp.data)
        self.assertTrue(b"2:1" in resp.data)
        self.assertTrue(b"1:2" in resp.data)
        self.assertTrue(self.team_two.short_name.encode("utf-8") in resp.data)
        self.assertTrue(self.player.name.encode("utf-8") in resp.data)

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.login()
        resp = self.client.get("/team/1000000000")
        self.assertEqual(resp.status_code, 404)
