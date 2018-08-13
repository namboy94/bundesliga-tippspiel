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
        self.incomplete_columns = [
            Player(team=self.team_one),
            Player(name="1")
        ]
        self.indexed = [
            (1, self.player),
            (2, Player(team=self.team_one, name="1")),
            (3, Player(team=self.team_two, name="2"))
        ]
        self.non_uniques = []  # No unique attributes
