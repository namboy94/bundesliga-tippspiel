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

import time
import requests
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.background.openligadb import update_match_data
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.match_data.Goal import Goal


class TestMatchDataUpdate(_TestFramework):
    """
    Unit test class that tests the match_data_getter script
    """

    def test_populating_twice(self):
        """
        Tests populating the database. Twice.
        :return: None
        """
        update_match_data(season="2018", league="bl1")
        self.assert_db_state()
        update_match_data(season="2018", league="bl1")
        self.assert_db_state()

    def test_icon_urls(self):
        """
        Tests if all team icon URLs are valid
        :return: None
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        update_match_data()
        for team in Team.query.all():
            for url in [team.icon_svg]:
                resp = requests.head(url, headers=headers)
                time.sleep(1)
                retry_count = 0
                while resp.status_code == 429 and retry_count < 5:
                    time.sleep(30)
                    resp = requests.head(url, headers=headers)
                    retry_count += 1
                self.assertEqual(200, resp.status_code)

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
                for team_abbreviation in [
                    match.home_team_abbreviation, match.away_team_abbreviation
                ]:
                    self.assertFalse(team_abbreviation in teams)
                    teams.append(team_abbreviation)

                goal_count = \
                    match.home_current_score + match.away_current_score
                goals = Goal.query.filter_by(
                    home_team_abbreviation=match.home_team_abbreviation,
                    away_team_abbreviation=match.away_team_abbreviation,
                    season=match.season
                ).all()
                self.assertEqual(goal_count, len(goals))

        all_teams = Team.query.all()
        self.assertEqual(len(all_teams), 18)
        for team in all_teams:
            self.assertTrue(len(team.name) <= 50)
            self.assertTrue(len(team.short_name) <= 16)
            self.assertTrue(len(team.abbreviation) == 3)

        fcb_tsg: Match = Match.query.get(("bl1", 2018, 1, "FCB", "TSG"))
        self.assertEqual(3, fcb_tsg.home_current_score)
        self.assertEqual(1, fcb_tsg.away_current_score)

        goals = Goal.query.filter_by(
            home_team_abbreviation=fcb_tsg.home_team_abbreviation,
            away_team_abbreviation=fcb_tsg.away_team_abbreviation,
            season=fcb_tsg.season
        ).all()
        self.assertEqual(len(goals), 4)
        self.assertEqual(goals[0].player.name, "Thomas Müller")

        fcb = fcb_tsg.home_team
        self.assertEqual(fcb.name, "FC Bayern München")
        self.assertEqual(fcb.short_name, "FC Bayern")
        self.assertEqual(fcb.abbreviation, "FCB")
