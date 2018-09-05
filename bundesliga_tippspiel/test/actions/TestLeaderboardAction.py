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

from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestLeaderboardAction(_ActionTestFramework):
    """
    Class that tests the Login action
    """

    def setUp(self):
        """
        Sets up users for testing
        :return: None
        """
        super().setUp()
        self.user_one = self.generate_sample_user(True)["user"]
        self.user_two = User(username="AA", email="AA", password_hash="AA",
                             confirmation_hash="AA", confirmed=True)
        self.user_three = User(username="BB", email="BB", password_hash="BB",
                               confirmation_hash="BB", confirmed=True)
        self.unconfirmed_user = self.generate_sample_user(False)["user"]
        self.team_one, self.team_two, _, _, _ = \
            self.generate_sample_match_data()
        self.match_one = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            home_current_score=1, away_current_score=1,
            started=True, finished=True
        )
        self.match_two = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=2, kickoff="2019-01-01:01:02:03",
            home_current_score=1, away_current_score=1,
            started=True, finished=True
        )
        self.match_three = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=3, kickoff="2019-01-01:01:02:03",
            home_current_score=1, away_current_score=1,
            started=True, finished=False
        )
        self.match_four = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=4, kickoff="2019-01-01:01:02:03",
            home_current_score=1, away_current_score=1,
            started=False, finished=False
        )

        self.db.session.add(self.match_one)
        self.db.session.add(self.match_two)
        self.db.session.add(self.match_three)
        self.db.session.add(self.match_four)
        self.db.session.add(self.user_two)
        self.db.session.add(self.user_three)
        self.db.session.commit()

        for user, home, away in [
            (self.user_one, 2, 2),
            (self.user_two, 1, 1),
            (self.user_three, 1, 0)
        ]:
            for match in [
                self.match_one,
                self.match_two,
                self.match_three,
                self.match_four
            ]:
                bet = Bet(
                    user_id=user.id, match_id=match.id,
                    home_score=home, away_score=away
                )
                self.db.session.add(bet)
                self.db.session.commit()

        self.db.session.commit()

    def generate_action(self) -> LeaderboardAction:
        """
        Generates a valid LeaderboardAction object
        :return: The generated LeaderboardAction
        """
        return LeaderboardAction.from_dict({})

    def test_leaderboard(self):
        """
        Tests that the leaderboard is generated correctly
        :return: None
        """
        leaderboard = self.action.execute()["leaderboard"]
        self.assertEqual(len(leaderboard), 3)
        self.assertEqual(leaderboard[0], (self.user_two, 30))
        self.assertEqual(leaderboard[1], (self.user_one, 24))
        self.assertEqual(leaderboard[2], (self.user_three, 6))

    def test_leaderboard_for_matchday(self):
        """
        Tests generating a leaderboard for a specific matchday
        :return: None
        """
        self.action.matchday = 1
        leaderboard = self.action.execute()["leaderboard"]
        self.assertEqual(len(leaderboard), 3)
        self.assertEqual(leaderboard[0], (self.user_two, 15))
        self.assertEqual(leaderboard[1], (self.user_one, 12))
        self.assertEqual(leaderboard[2], (self.user_three, 3))
