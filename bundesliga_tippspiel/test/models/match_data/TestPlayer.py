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

from bundesliga_tippspiel.test.models.ModelTestFramework import \
    ModelTestFramework
from bundesliga_tippspiel.models.match_data.Player import Player


class TestPlayer(ModelTestFramework):
    """
    Tests the Player SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Player

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Player(team=self.team_one),
            Player(name="1")
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.player),
            (2, Player(team=self.team_one, name="1")),
            (3, Player(team=self.team_two, name="2"))
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
            (lambda: Player.query.filter_by(id=self.player.id).first(),
             self.player)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.player, [self.goal])
        ])