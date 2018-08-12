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
from bundesliga_tippspiel.models.match_data.Goal import Goal


class TestGoal(ModelTestFramework):
    """
    Tests the Goal SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.incomplete_columns = [
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
        ]
        self.invalid_constructors = [
            lambda: Goal(match="Match", player=self.player,
                         home_score=1, away_score=1, minute=1),
            lambda: Goal(match=self.match, player="Player",
                         home_score=1, away_score=1, minute=1),
            lambda: Goal(match=1, player=self.player,
                         home_score=1, away_score=1, minute=1)
        ]
        self.indexed = [
            (1, self.goal),
            (2, Goal(match=self.match, player=self.player,
                     minute=1, home_score=1, away_score=1)),
            (3, Goal(match=self.match, player=self.player,
                     minute=2, home_score=2, away_score=1))
        ]
        self.non_uniques = []  # No unique attributes
