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
from bundesliga_tippspiel.db.user_generated.SeasonWinner import SeasonWinner
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.db.ModelTestFramework import \
    _ModelTestFramework


class TestSeasonWinner(_ModelTestFramework):
    """
    Tests the SeasonWinner SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = SeasonWinner
        self.winner = SeasonWinner(
            user=self.user_one,
            season=2010,
            league="bl1"
        )
        db.session.add(self.winner)
        db.session.commit()

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            # SeasonWinner(user=self.user_one),
            SeasonWinner(season=2000)
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            SeasonWinner(user=self.user_two, season=2010)
        ])

    def test_cascades(self):
        """
        Tests if cascade deletes work correctly
        :return: None
        """
        self.assertEqual(len(SeasonWinner.query.all()), 1)
        db.session.delete(self.user_one)
        self.assertEqual(len(SeasonWinner.query.all()), 0)

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.winner.__json__(False)
        without_children.update({
            "user": self.winner.user.__json__(True, ["season_winners"])
        })
        self.assertEqual(
            self.winner.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.winner)

    def test_season_string(self):
        """
        Tests the season string
        :return: None
        """
        self.assertEqual(self.winner.season_string, "Bundesliga 2010/11")
