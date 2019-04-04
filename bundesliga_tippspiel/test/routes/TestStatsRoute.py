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


class TestStatsRoute(_RouteTestFramework):
    """
    Class that tests the /stats route
    """

    def setUp(self):
        """
        Generates sample match data
        :return: None
        """
        super().setUp()
        team_one, team_two, _, match, _ = self.generate_sample_match_data()
        finished_match = Match(
            home_team=team_one, away_team=team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=True, finished=True,
            home_current_score=0, away_current_score=0
        )
        self.db.session.add(finished_match)
        self.db.session.commit()
        self.generate_sample_bet(self.user, match)
        self.generate_sample_bet(self.user, finished_match)

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
        return "/stats", ["GET"], "Statistiken", True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        pass

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        pass

    def test_malformed_data(self):
        """
        Tests that malformed data in the request is handled appropriately
        :return: None
        """
        pass
