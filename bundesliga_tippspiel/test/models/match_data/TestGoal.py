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
from bundesliga_tippspiel.models.match_data.Goal import Goal


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

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.goal),
            (2, Goal(match=self.match, player=self.player,
                     minute=1, home_score=1, away_score=1)),
            (3, Goal(match=self.match, player=self.player,
                     minute=2, home_score=2, away_score=1))
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
            (lambda: Goal.query.filter_by(id=self.goal.id).first(), self.goal)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.goal, [])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.goal.__json__(False)
        without_children.update({
            "match": self.goal.match.__json__(True),
            "player": self.goal.player.__json__(True)
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
