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

# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework
from bundesliga_tippspiel.models.match_data.Match import Match


class TestMatch(_ModelTestFramework):
    """
    Tests the Match SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Match

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Match(away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1,
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False)
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.match),
            (2, Match(home_team=self.team_one, away_team=self.team_two,
                      matchday=1, kickoff="2019-01-01:01:02:03",
                      started=False, finished=False))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        # TODO Fix unique constraint
        self._test_uniqueness([
            # Match(home_team=self.match.home_team,
            #       away_team=self.match.away_team,
            #       matchday=self.match.matchday,
            #       kickoff="2019-01-01:01:02:03",
            #       started=False, finished=False)
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Match.query.filter_by(id=self.match.id).first(),
             self.match)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.match, [self.goal])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.match.__json__(False)
        without_children.update({
            "home_team": self.match.home_team.__json__(True),
            "away_team": self.match.away_team.__json__(True)
        })
        self.assertEqual(
            self.match.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.match)
