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

from bundesliga_tippspiel.test.TestFramework import TestFramework
from bundesliga_tippspiel.models.match_data.Goal import Goal


class TestGoal(TestFramework):
    """
    Tests the Goal SQL model
    """

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """

        _, _, player, match, _ = self.generate_sample_match_data()

        for g in [
            Goal(match=None, player=player, minute=1,
                 home_score=1, away_score=1),
            Goal(match=match, player=None, minute=1,
                 home_score=1, away_score=1),
            Goal(match=match, player=player, minute=None,
                 home_score=1, away_score=1),
            Goal(match=match, player=player, minute=1,
                 home_score=None, away_score=1),
            Goal(match=match, player=player, minute=1,
                 home_score=1, away_score=None)
        ]:
            self._test_invalid_db_add(g)

    def test_invalid_column_types(self):
        """
        Tests that invalid types for column data is handled correctly
        :return: None
        """

        _, _, player, match, _ = self.generate_sample_match_data()

        for constructor_call in [
            lambda: Goal(match="Match", player=player,
                         home_score=1, away_score=1, minute=1),
            lambda: Goal(match=match, player="Player",
                         home_score=1, away_score=1, minute=1),
            lambda: Goal(match=1, player=player,
                         home_score=1, away_score=1, minute=1)
        ]:
            try:
                constructor_call()
                self.fail()
            except AttributeError:
                pass
