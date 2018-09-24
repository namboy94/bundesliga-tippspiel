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

from datetime import datetime, timedelta
from bundesliga_tippspiel.models.match_data.Match import Match
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestMatch(_ModelTestFramework):
    """
    Tests the Match SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Match

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Match(away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  kickoff="2019-01-01:01:02:03",
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1,
                  started=False, finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  finished=False),
            Match(home_team=self.team_one, away_team=self.team_two,
                  matchday=1, kickoff="2019-01-01:01:02:03",
                  started=False)
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.match),
            (2, Match(home_team=self.team_one, away_team=self.team_two,
                      matchday=1, kickoff="2019-01-01:01:02:03",
                      started=False, finished=False))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        # TODO Fix unique constraint
        self._test_uniqueness([
            # Match(home_team=self.match.home_team,
            #       away_team=self.match.away_team,
            #       matchday=self.match.matchday,
            #       kickoff="2019-01-01:01:02:03",
            #       started=False, finished=False)
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Match.query.filter_by(id=self.match.id).first(),
             self.match)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.match, [self.goal])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.match.__json__(False)
        without_children.update({
            "home_team": self.match.home_team.__json__(True),
            "away_team": self.match.away_team.__json__(True)
        })
        self.assertEqual(
            self.match.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.match)

    def test_kickoff_datetime_conversion(self):
        """
        Tests the kickoff_datetime metod
        :return: None
        """
        self.match.kickoff = "2018-01-02:22-30-00"
        date = datetime(year=2018, month=1, day=2, hour=22, minute=30)
        self.assertEqual(date, self.match.kickoff_datetime)

    def test_minute_representation(self):
        """
        Tests the representation of the current minute of the match
        :return: None
        """
        now = datetime.utcnow()

        match = Match(finished=True, kickoff=now.strftime("%Y-%m-%d:%H-%M-%S"))
        self.assertEqual(match.minute_display, "Ende")

        match.finished = False
        match.kickoff = (now + timedelta(days=1)).strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "-")

        match.kickoff = (now - timedelta(days=1)).strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "90.")

        match.kickoff = (now - timedelta(minutes=20))\
            .strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "21.")

        match.kickoff = (now - timedelta(minutes=46)) \
            .strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "45.")

        match.kickoff = (now - timedelta(minutes=50)) \
            .strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "HZ")

        match.kickoff = (now - timedelta(minutes=80)) \
            .strftime("%Y-%m-%d:%H-%M-%S")
        self.assertEqual(match.minute_display, "61.")

    def test_score_representations(self):
        """
        Tests the score representation attributes
        :return: None
        """
        match = Match(
            home_ht_score=0, away_ht_score=1,
            home_ft_score=2, away_ft_score=3,
            home_current_score=4, away_current_score=5
        )
        self.assertEqual(match.ht_score, "0:1")
        self.assertEqual(match.ft_score, "2:3")
        self.assertEqual(match.current_score, "4:5")
