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

import requests
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.utils.match_data_getter import update_db_data
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.models.match_data.Goal import Goal


class TestMatchDataGetter(_TestFramework):
    """
    Unit test class that tests the match_data_getter script
    """

    @_TestFramework.online_required
    def test_populating_twice(self):
        """
        Tests populating the database. Twice.
        :return: None
        """
        update_db_data()
        self.assert_db_state()
        update_db_data()
        self.assert_db_state()

    @_TestFramework.online_required
    def test_icon_urls(self):
        """
        Tests if all team icon URLs are valid
        :return: None
        """
        update_db_data()
        for team in Team.query.all():
            for url in [team.icon_svg, team.icon_png]:
                resp = requests.head(url)
                self.assertEqual(resp.status_code, 200)

    def assert_db_state(self):
        """
        Performs multiple assertions on a filled database
        :return: None
        """
        for matchday in range(1, 35):

            teams = []

            matches = Match.query.filter_by(matchday=matchday).all()
            self.assertEqual(len(matches), 9)

            for match in matches:
                for team_id in [match.home_team.id, match.away_team.id]:
                    self.assertFalse(team_id in teams)
                    teams.append(team_id)

                goal_count = \
                    match.home_current_score + match.away_current_score
                goals = Goal.query.filter_by(match_id=match.id).all()
                self.assertEqual(goal_count, len(goals))

        all_teams = Team.query.all()
        self.assertEqual(len(all_teams), 18)
        for team in all_teams:
            self.assertTrue(len(team.name) <= 50)
            self.assertTrue(len(team.short_name) <= 16)
            self.assertTrue(len(team.abbreviation) == 3)

        fcb_tsg = Match.query.get(51121)  # type: Match
        self.assertEqual(3, fcb_tsg.home_current_score)
        self.assertEqual(1, fcb_tsg.away_current_score)

        goals = Goal.query.filter_by(match_id=fcb_tsg.id).all()
        self.assertEqual(len(goals), 4)
        self.assertEqual(goals[0].player.name, "Thomas Müller")

        fcb = fcb_tsg.home_team
        self.assertEqual(fcb.name, "FC Bayern München")
        self.assertEqual(fcb.short_name, "FC Bayern")
        self.assertEqual(fcb.abbreviation, "FCB")
