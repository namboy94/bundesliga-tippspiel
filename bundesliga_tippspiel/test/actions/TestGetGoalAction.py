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

from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.GetActionTestFramework import \
    _GetActionTestFramework


class TestGetGoalAction(_GetActionTestFramework):
    """
    Class that tests the GetGoal action
    """

    @property
    def action_cls(self) -> type(GetGoalAction):
        """
        :return: The tested Action class
        """
        return GetGoalAction

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        # All
        result = self.action.execute()
        self.assertEqual(len(result["goals"]), 2)
        self.assertFalse("goal" in result)

        # By ID
        self.action.id = self.goal_one.id
        result = self.action.execute()
        self.assertEqual(result["goal"], self.goal_one)
        self.assertEqual(result["goals"], [self.goal_one])

        # Filtered
        self.action.id = None
        self.action.matchday = self.goal_one.match.matchday
        self.action.match_id = self.goal_one.match_id
        self.action.player_id = self.goal_one.player_id
        self.action.team_id = self.goal_one.player.team_id

        filtered = self.action.execute()["goals"]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], self.goal_one)

    def test_using_filter_and_id(self):
        """
        Tests that using an ID and an explicit filter does not work
        :return: None
        """
        self.action.id = self.goal_one.id
        self.action.matchday = self.goal_one.match.matchday

        self.failed_execute("Can't filter specific ID")
