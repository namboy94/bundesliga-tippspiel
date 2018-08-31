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

from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestGetBetAction(_ActionTestFramework):
    """
    Class that tests the GetBet action
    """

    def setUp(self):
        """
        Sets up sample data for testing purposes
        :return: None
        """
        super().setUp()
        self.team_one, self.team_two, _, self.match_one, _ = \
            self.generate_sample_match_data()
        self.match_two = Match(
            home_team=self.team_two,
            away_team=self.team_one,
            matchday=18,
            kickoff="2019-01-01:01:02:03",
            started=False,
            finished=False
        )
        self.db.session.add(self.match_two)
        self.db.session.commit()
        self.user_one, self.user_two = self.generate_sample_users()
        self.user_one = self.user_one["user"]
        self.user_two = self.user_two["user"]
        self.bet_one = self.generate_sample_bet(self.user_one, self.match_one)
        self.bet_two = self.generate_sample_bet(self.user_two, self.match_one)
        self.bet_three = \
            self.generate_sample_bet(self.user_one, self.match_two)

    def generate_action(self) -> GetBetAction:
        """
        Generates a valid GetBetAction object
        :return: The generated GetBetAction
        """
        return GetBetAction()

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        # All
        self.assertEqual(len(self.action.execute()["bets"]), 3)

        # By ID
        self.action.id = self.bet_one.id
        self.assertEqual(self.action.execute()["bets"], self.bet_one)

        # Filtered
        self.action.id = None
        self.action.matchday = self.bet_one.match.matchday
        self.action.user_id = self.user_one.id
        self.action.match_id = self.bet_one.match.id
        self.assertEqual(self.action.execute()["bets"][0], self.bet_one)
