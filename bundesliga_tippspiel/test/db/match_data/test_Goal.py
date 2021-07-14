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

from jerrycan.base import db
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.db.ModelTestFramework import \
    _ModelTestFramework
from bundesliga_tippspiel.db.match_data.Goal import Goal


class TestGoal(_ModelTestFramework):
    """
    Tests the Goal SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Goal

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Goal(match=None, player=self.player, minute=1,
                 home_score=1, away_score=1),
            Goal(match=self.match, player=None, minute=1,
                 home_score=1, away_score=1),
            Goal(match=self.match, player=self.player, minute=None,
                 home_score=1, away_score=1),
            Goal(match=self.match, player=self.player, minute=1,
                 home_score=None, away_score=1),
            Goal(match=self.match, player=self.player, minute=1,
                 home_score=1, away_score=None)
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Goal.query.filter_by(
                season=self.goal.season,
                home_team_abbreviation=self.goal.home_team_abbreviation,
                away_team_abbreviation=self.goal.away_team_abbreviation,
                home_score=self.goal.home_score,
                away_score=self.goal.away_score
            ).first(), self.goal)
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.goal.__json__(False)
        without_children.update({
            "match": self.goal.match.__json__(True, ["goals"]),
            "player": self.goal.player.__json__(True, ["goals"])
         })
        self.assertEqual(
            self.goal.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.goal)

    def test_cascades(self):
        """
        Tests if cascade deletes work correctly
        :return: None
        """
        self.assertEqual(len(Goal.query.all()), 1)
        db.session.delete(self.match)
        self.assertEqual(len(Goal.query.all()), 0)
        self.tearDown()
        self.setUp()
        self.assertEqual(len(Goal.query.all()), 1)
        db.session.delete(self.player)
        self.assertEqual(len(Goal.query.all()), 0)
