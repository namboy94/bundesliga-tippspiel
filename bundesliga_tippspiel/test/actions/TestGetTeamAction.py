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

from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.GetActionTestFramework import \
    _GetActionTestFramework


class TestGetTeamAction(_GetActionTestFramework):
    """
    Class that tests the GetTeam action
    """

    @property
    def action_cls(self) -> type(GetTeamAction):
        """
        :return: The tested Action class
        """
        return GetTeamAction

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        # All
        result = self.action.execute()
        self.assertEqual(len(result["teams"]), 3)
        self.assertFalse("team" in result)

        # By ID
        self.action.id = self.team_one.id
        result = self.action.execute()
        self.assertEqual(result["team"], self.team_one)
        self.assertEqual(result["teams"], [self.team_one])

        # Filtered
        # Has no filters

    def test_using_filter_and_id(self):
        """
        Tests that using an ID and an explicit filter does not work
        :return: None
        """
        pass  # Has no filters
