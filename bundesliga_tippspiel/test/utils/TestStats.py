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
from bundesliga_tippspiel.models.match_data.Match import Match
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.utils.stats import get_team_points_data, \
    generate_team_points_table, get_total_points_per_team


class TestStats(_TestFramework):
    """
    Tests stats generation
    """

    def test_generating_team_points_data(self):
        """
        Tests generating team points data
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
            home_current_score=2, away_current_score=1
        )
        match_two = Match(
            home_team=team_one, away_team=team_two,
            matchday=2, kickoff="2019-01-01:01:02:03",
            started=True, finished=True,
            home_current_score=0, away_current_score=0
        )
        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.add(user_two)
        bet_one = self.generate_sample_bet(user_one, match_one)
        bet_two = self.generate_sample_bet(user_one, match_two)
        self.db.session.commit()

        total_points = bet_one.evaluate(True) + bet_two.evaluate(True)

        all_stats = get_team_points_data()
        team_points = get_total_points_per_team()

        table_one = generate_team_points_table(all_stats[user_one])
        table_two = generate_team_points_table(all_stats[user_two])
        table_all = generate_team_points_table(team_points)

        self.assertNotEqual(table_one, table_two)
        self.assertEqual(table_one, table_all)
        self.assertNotEqual(table_two, table_all)

        self.assertEqual(table_all[0][1], total_points)
