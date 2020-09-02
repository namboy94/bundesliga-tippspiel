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
from puffotter.flask.base import db
from bundesliga_tippspiel.db.user_generated.SeasonTeamBet import \
    SeasonTeamBet, SeasonTeamBetType
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestSeasonTeamBetsRoute(_RouteTestFramework):
    """
    Class that tests the /season_team_bets route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return:
        """
        super().setUp()
        _, _, _, self.match, _ = self.generate_sample_match_data()
        self.match.finished = False
        self.match.started = False
        db.session.commit()

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
        return "/bets/season_team_bets", ["POST"], None, True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        self.assertEqual(len(SeasonTeamBet.query.all()), 0)
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            SeasonTeamBetType.MOST_GOALS_CONCEDED.name:
                str(self.match.home_team_id),
            SeasonTeamBetType.LEAST_GOALS_CONCEDED.name:
                str(self.match.away_team_id)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(SeasonTeamBet.query.all()), 2)

        self.assertEqual(SeasonTeamBet.query.all()[0].bet_type,
                         SeasonTeamBetType.MOST_GOALS_CONCEDED)
        self.assertEqual(SeasonTeamBet.query.all()[0].team_id,
                         self.match.home_team_id)
        self.assertEqual(SeasonTeamBet.query.all()[1].bet_type,
                         SeasonTeamBetType.LEAST_GOALS_CONCEDED)
        self.assertEqual(SeasonTeamBet.query.all()[1].team_id,
                         self.match.away_team_id)

        resp = self.client.post(self.route_path, follow_redirects=True, data={
            SeasonTeamBetType.MOST_GOALS_SCORED.name:
                str(self.match.home_team_id),
            SeasonTeamBetType.LEAST_GOALS_CONCEDED.name:
                str(self.match.home_team_id)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(SeasonTeamBet.query.all()), 3)

        self.assertEqual(SeasonTeamBet.query.all()[1].bet_type,
                         SeasonTeamBetType.LEAST_GOALS_CONCEDED)
        self.assertEqual(SeasonTeamBet.query.all()[1].team_id,
                         self.match.home_team_id)
        self.assertEqual(SeasonTeamBet.query.all()[2].bet_type,
                         SeasonTeamBetType.MOST_GOALS_SCORED)
        self.assertEqual(SeasonTeamBet.query.all()[2].team_id,
                         self.match.home_team_id)

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.login()
        self.assertEqual(len(SeasonTeamBet.query.all()), 0)
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            SeasonTeamBetType.MOST_GOALS_CONCEDED.name: "9000",
            "Lala": str(self.match.away_team_id)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(SeasonTeamBet.query.all()), 0)

        self.match.matchday = 18
        db.session.commit()
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            SeasonTeamBetType.MOST_GOALS_CONCEDED.name:
                str(self.match.home_team_id),
            SeasonTeamBetType.LEAST_GOALS_CONCEDED.name:
                str(self.match.away_team_id)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(SeasonTeamBet.query.all()), 0)

    def test_malformed_data(self):
        """
        Tests that malformed data in the request is handled appropriately
        :return: None
        """
        pass
