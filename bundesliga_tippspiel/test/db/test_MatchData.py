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
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class TestMatchData(_TestFramework):
    """
    Class that tests the various match data models
    """

    def test_model_relations(self):
        """
        Tests the relations between the models
        :return: None
        """
        team_one, team_two, player, match, goal = \
            self.generate_sample_match_data()

        self.assertEqual(player.team, team_one)
        self.assertEqual(match.home_team, team_one)
        self.assertEqual(match.away_team, team_two)
        self.assertEqual(goal.match, match)
        self.assertEqual(goal.player, player)
        self.assertNotEqual(team_one, team_two)
