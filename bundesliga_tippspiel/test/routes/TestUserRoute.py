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

from bundesliga_tippspiel.models.auth.User import User
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestUserRoute(_RouteTestFramework):
    """
    Class that tests the /user route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return:
        """
        super().setUp()
        self.second_user = User(username="AA", email="AA", password_hash="AA",
                                confirmation_hash="AA", confirmed=True)
        team_one, team_two, _, _, _ = self.generate_sample_match_data()
        self.db.session.add(self.second_user)
        self.db.session.add(Match(
            home_team=team_one, away_team=team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=False
        ))
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
        return "/user/{}".format(self.second_user.id), \
               [], \
               "<h1>{}</h1>".format(self.second_user.username), \
               True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        resp = self.client.get(self.route_path)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b"canvas" in resp.data)

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.login()
        resp = self.client.get("/user/1000000000")
        self.assertEqual(resp.status_code, 404)
