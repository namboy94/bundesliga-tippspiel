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
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Team import Team
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestBetsRoute(_RouteTestFramework):
    """
    Class that tests the /bets route
    """

    def setUp(self):
        """
        Sets up data for the tests
        :return:
        """
        super().setUp()
        self.team_one, self.team_two, zero, old_match, _ = \
            self.generate_sample_match_data()
        self.team_three = Team(
            name="ZZ", short_name="ZZ", abbreviation="ZZ",
            icon_svg="ZZ", icon_png="ZZ"
        )
        self.db.session.add(self.team_three)
        self.db.session.delete(old_match)
        self.db.session.commit()
        self.match_one = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01-02-03",
            started=False, finished=True,
            home_current_score=0, away_current_score=0,
            season=self.config.season(),
            league=self.config.OPENLIGADB_LEAGUE
        )
        self.match_two = Match(
            home_team=self.team_two, away_team=self.team_one,
            matchday=1, kickoff="2019-01-01:01-02-03",
            started=False, finished=False,
            home_current_score=0, away_current_score=0,
            season=self.config.season(),
            league=self.config.OPENLIGADB_LEAGUE
        )
        self.match_three = Match(
            home_team=self.team_one, away_team=self.team_three,
            matchday=1, kickoff="2019-01-01:01-02-03",
            started=True, finished=False,
            home_current_score=1, away_current_score=3,
            season=self.config.season(),
            league=self.config.OPENLIGADB_LEAGUE
        )
        self.db.session.add(self.match_one)
        self.db.session.add(self.match_two)
        self.db.session.add(self.match_three)
        self.db.session.delete(zero)
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
        return "/bets", ["POST"], "Spieltag", True

    def test_getting_specific_matchday(self):
        """
        Tests retrieving a specific matchday
        :return: None
        """
        self.login()
        resp = self.client.get(
            f"{self.route_path}/{self.match_one.league}/"
            f"{self.match_one.season}/{self.match_one.matchday}"
        )
        self.assertTrue(
            "Spieltag {}".format(self.match_one.matchday).encode("utf-8") in
            resp.data
        )

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.login()
        self.assertEqual(len(Bet.query.all()), 0)
        self.match_one.kickoff = "3000-01-01:01-01-01"
        self.db.session.commit()
        match_id = f"{self.match_one.league}_{self.match_one.season}_" \
                   f"{self.match_one.matchday}_" \
                   f"{self.match_one.home_team_abbreviation}_" \
                   f"{self.match_one.away_team_abbreviation}"
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            f"{match_id}_home": 1,
            f"{match_id}_away": "2"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Bet.query.all()), 1)
        self.assertEqual(Bet.query.all()[0].home_score, 1)
        self.assertEqual(Bet.query.all()[0].away_score, 2)

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
