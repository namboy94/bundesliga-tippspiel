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
from bundesliga_tippspiel.models.auth.User import User
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.utils.chart_data import generate_leaderboard_data


class TestChartData(_TestFramework):
    """
    Tests chart data generation
    """

    def test_generating_leaderboard_data(self):
        """
        Tests generating leaderboard data
        :return: None
        """
        user_one = self.generate_sample_user(True)["user"]
        user_two = User(username="AA", email="AA", password_hash="AA",
                                 confirmation_hash="AA", confirmed=True)

        team_one, team_two, _, old_match, _ = self.generate_sample_match_data()
        match_one = Match(
            home_team=team_one, away_team=team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=True, finished=True,
            home_current_score=1, away_current_score=2
        )
        match_two = Match(
            home_team=team_one, away_team=team_two,
            matchday=2, kickoff="2019-01-01:01:02:03",
            started=False, finished=False,
            home_current_score=0, away_current_score=0
        )
        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.add(user_two)
        self.generate_sample_bet(user_one, match_one)
        self.generate_sample_bet(user_one, match_two)
        self.generate_sample_bet(user_two, match_one)
        self.generate_sample_bet(user_two, match_two)
        self.db.session.commit()

        matchday, data = generate_leaderboard_data()

        self.assertEqual(matchday, 2)
        self.assertEqual(len(data), 2)
