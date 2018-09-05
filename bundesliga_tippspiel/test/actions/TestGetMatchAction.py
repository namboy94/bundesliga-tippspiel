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

from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.GetActionTestFramework import \
    _GetActionTestFramework


class TestGetMatchAction(_GetActionTestFramework):
    """
    Class that tests the GetMatch action
    """

    @property
    def action_cls(self) -> type(GetMatchAction):
        """
        :return: The tested Action class
        """
        return GetMatchAction

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        # All
        result = self.action.execute()
        self.assertEqual(len(result["matches"]), 2)
        self.assertFalse("match" in result)

        # By ID
        self.action.id = self.match_one.id
        result = self.action.execute()
        self.assertEqual(result["match"], self.match_one)
        self.assertEqual(result["matches"], [self.match_one])

        # Filtered
        self.action.id = None
        self.action.matchday = self.match_two.matchday
        filtered = self.action.execute()["matches"]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], self.match_two)

        self.action.matchday = None
        self.action.team_id = self.team_one.id
        filtered = self.action.execute()["matches"]
        self.assertEqual(len(filtered), 2)

    def test_using_filter_and_id(self):
        """
        Tests that using an ID and an explicit filter does not work
        :return: None
        """
        self.action.id = self.match_one.id
        self.action.matchday = self.match_one.matchday

        self.failed_execute("Can't filter specific ID")
