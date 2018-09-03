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

from bundesliga_tippspiel.utils.json import jsonify_models
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class TestJson(_TestFramework):
    """
    Unit test class that tests the json methods used for the API
    """

    def test_jsonifying(self):
        """
        Tests jsonifying some objects
        :return: None
        """
        team_one, team_two, player, match, goal = \
            self.generate_sample_match_data()

        for deep in [False, True]:
            for raw, expected in [
                ({"1": 1, "2": [1, 2, 3]}, {"1": 1, "2": [1, 2, 3]}),
                ({"1": {"1": {"1": None}}}, {"1": {"1": {"1": None}}}),
                (
                    {"a": team_one, "B": team_two, "c": player, "D": goal},
                    {"a": team_one.__json__(deep),
                     "B": team_two.__json__(deep),
                     "c": player.__json__(deep),
                     "D": goal.__json__(deep)}
                )
            ]:
                jsonified = jsonify_models(raw, deep)
                self.assertEqual(jsonified, expected)
