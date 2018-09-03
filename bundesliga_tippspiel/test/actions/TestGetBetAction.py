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

from flask_login import logout_user
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.GetActionTestFramework import \
    _GetActionTestFramework


class TestGetBetAction(_GetActionTestFramework):
    """
    Class that tests the GetBet action
    """

    @property
    def action_cls(self) -> type(GetBetAction):
        """
        :return: The tested Action class
        """
        return GetBetAction

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        with self.context:
            self.login_user(self.user_one)

            # All
            result = self.action.execute()
            self.assertEqual(len(result["bets"]), 3)
            self.assertFalse("bet" in result)

            # By ID
            self.action.id = self.bet_one.id
            result = self.action.execute()
            self.assertEqual(result["bet"], self.bet_one)
            self.assertEqual(result["bets"], [self.bet_one])

            # Filtered
            self.action.id = None
            self.action.matchday = self.bet_one.match.matchday
            self.action.user_id = self.user_one.id
            self.action.match_id = self.bet_one.match.id
            filtered = self.action.execute()["bets"]

            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0], self.bet_one)

            # Reset and switch user
            logout_user()
            self.user_two.confirmed = True
            self.login_user(self.user_two)
            self.action.id = None
            self.action.matchday = None
            self.action.user_id = None
            self.action.match_id = None

            # All
            self.assertEqual(len(self.action.execute()["bets"]), 2)

            # By ID
            self.action.id = self.bet_three.id
            self.failed_execute("ID not accessible", 401)

            # Filtered
            self.action.id = None
            self.action.matchday = self.bet_one.match.matchday
            self.action.user_id = self.user_one.id
            self.action.match_id = self.bet_one.match.id
            filtered = self.action.execute()["bets"]

            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0], self.bet_one)

    def test_fetching_by_match(self):
        """
        Explicitly search by match ID, since there was a bug once
        :return: None
        """
        self.action.match_id = self.bet_one.match_id
        filtered = self.action.execute()["bets"]

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0], self.bet_one)

        self.action.user_id = self.bet_one.user.id
        filtered = self.action.execute()["bets"]

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], self.bet_one)

    def test_using_filter_and_id(self):
        """
        Tests that using an ID and an explicit filter does not work
        :return: None
        """
        self.action.id = self.bet_one.id
        self.action.matchday = self.match_one.matchday

        self.failed_execute("Can't filter specific ID")
