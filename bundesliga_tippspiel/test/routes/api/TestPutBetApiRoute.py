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
from bundesliga_tippspiel.models.match_data.Match import Match
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestPutBetApiRoute(_ApiRouteTestFramework):
    """
    Tests the /bet PUT API route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return: None
        """
        super().setUp()
        self.team_one, self.team_two, _, _, _ = \
            self.generate_sample_match_data()
        self.match_one = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=True
        )
        self.match_two = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=False
        )
        self.match_three = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=True, finished=False
        )
        self.db.session.add(self.match_one)
        self.db.session.add(self.match_two)
        self.db.session.add(self.match_three)
        self.db.session.commit()

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/bet", ["PUT"], True

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        resp = self.decode_data(self.client.put(
            self.route_path,
            headers=self.generate_headers(),
            json={
                "{}-home".format(self.match_one.id): 2,
                "{}-away".format(self.match_one.id): 1,
                "{}-home".format(self.match_two.id): "A",
                "{}-away".format(self.match_two.id): 1,
                "{}-home".format(self.match_three.id): 2,
                "{}-away".format(self.match_three.id): 1,
            }
        ))
        self.assertEqual(resp["status"], "ok")
        self.assertEqual(resp["data"], {
            "new": 1,
            "updated": 0,
            "invalid": 2
        })

        resp = self.decode_data(self.client.put(
            self.route_path,
            headers=self.generate_headers(),
            json={
                "{}-home".format(self.match_one.id): 5,
                "{}-away".format(self.match_one.id): 0,
            }
        ))
        self.assertEqual(resp["status"], "ok")
        self.assertEqual(resp["data"], {
            "new": 0,
            "updated": 1,
            "invalid": 0
        })

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        pass
