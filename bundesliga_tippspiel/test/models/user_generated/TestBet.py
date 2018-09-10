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

from bundesliga_tippspiel.models.user_generated.Bet import Bet
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestBet(_ModelTestFramework):
    """
    Tests the Bet SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Bet

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Bet(match=self.match, home_score=3, away_score=1),
            Bet(user=self.user_one, home_score=3, away_score=1),
            Bet(user=self.user_one, match=self.match, away_score=1),
            Bet(user=self.user_one, match=self.match, home_score=3)
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.bet),
            (2, Bet(
                user=self.user_one,
                match=self.match,
                home_score=3,
                away_score=1
            ))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        # No unique stuff
        pass

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Bet.query.filter_by(id=self.bet.id).first(),
             self.bet),
            (lambda: Bet.query.filter_by(
                user_id=self.bet.user_id, match_id=self.bet.match_id
            ).first(),
             self.bet)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.bet, [])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.bet.__json__(False)
        without_children.update({
            "user": self.bet.user.__json__(True),
            "match": self.bet.match.__json__(True)
        })
        self.assertEqual(
            self.bet.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.bet)

    def test_evaluating_bet_result(self):
        """
        Tests evaluating the results of a bet
        :return: None
        """
        self.bet.home_score = 0
        self.bet.away_score = 0
        self.bet.match.home_current_score = 0
        self.bet.match.away_current_score = 0
        self.assertEqual(self.bet.evaluate(), 3 + 5 + 7)  # 0:0 | 0:0

        self.bet.home_score = 2
        self.assertEqual(self.bet.evaluate(), 3)  # 2:0 | 0:0

        self.bet.match.away_current_score = 2
        self.assertEqual(self.bet.evaluate(), 0)  # 2:0 | 0:2

        self.bet.match.home_current_score = 2
        self.bet.match.away_current_score = 0
        self.assertEqual(self.bet.evaluate(), 3 + 5 + 7)  # 2:0 | 2:0

        self.bet.away_score = 1
        self.assertEqual(self.bet.evaluate(), 3 + 7)  # 2:1 | 2:0

        self.bet.home_score = 1
        self.assertEqual(self.bet.evaluate(), 0)  # 1:1 | 2:0

        self.bet.away_score = 1
        self.bet.match.away_current_score = 2
        self.assertEqual(self.bet.evaluate(), 5 + 7)  # 1:1 | 2:2

        self.bet.match.home_current_score = 1
        self.bet.match.away_current_score = 3
        self.assertEqual(self.bet.evaluate(), 3)  # 1:1 | 1:3

    def test_evaluating_unfinished_games(self):
        """
        Tests that evaluating unfinished games behaves correctly
        :return: None
        """
        self.bet.home_score = 0
        self.bet.away_score = 0
        self.bet.match.home_current_score = 0
        self.bet.match.away_current_score = 0
        self.bet.match.finished = False
        self.assertEqual(self.bet.evaluate(), 15)
        self.assertEqual(self.bet.evaluate(True), 0)
