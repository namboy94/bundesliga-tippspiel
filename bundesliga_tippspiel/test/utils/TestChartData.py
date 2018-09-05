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
from bundesliga_tippspiel.models.match_data.Match import Match

from bundesliga_tippspiel.models.auth.User import User
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

        team_one, team_two, _, match, _ = self.generate_sample_match_data()
        self.db.session.add(Match(
            home_team=team_one, away_team=team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=False
        ))
        self.db.session.add(user_two)
        self.generate_sample_bet(user_one, match)
        self.generate_sample_bet(user_two, match)
        self.db.session.commit()

        matchday, data = generate_leaderboard_data()

        self.assertEqual(matchday, 1)
        self.assertEqual(len(data), 2)
