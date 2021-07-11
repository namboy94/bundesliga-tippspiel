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

from unittest import mock
from datetime import datetime, timedelta
from jerrycan.db.User import User
from jerrycan.base import db
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.db.ModelTestFramework import \
    _ModelTestFramework


class TestReminderSettings(_ModelTestFramework):
    """
    Tests the ReminderSettings SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = ReminderSettings

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            ReminderSettings(user=self.user_two),
            ReminderSettings(reminder_type=ReminderType.EMAIL)
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            ReminderSettings(
                user=self.user_one, reminder_type=ReminderType.EMAIL
            )
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: ReminderSettings.query.filter_by(
                user_id=self.reminder.user_id,
                reminder_type=self.reminder.reminder_type
            ).first(),
             self.reminder)
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.reminder.__json__(False)
        without_children.update({
            "user": self.reminder.user.__json__(True, ["reminder_settings"])
        })
        self.assertEqual(
            self.reminder.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.reminder)

    def test_due(self):
        """
        Tests if due matches can be found correctly

        Dates:
        Now ----- Reminder 1 ----- Match 1 ----- Reminder 2 ----- Match 2
        -0----------10min-----------30min-----------60min---------120min-
        :return: None
        """
        now = datetime.utcnow()
        new_user = User(username="Z", email="Z", confirmed=True,
                        password_hash="Z", confirmation_hash="Z")
        reminder_one = ReminderSettings(
            user=self.user_two, reminder_time=600,
            reminder_type=ReminderType.EMAIL
        )
        reminder_two = ReminderSettings(
            user=new_user, reminder_time=3600, reminder_type=ReminderType.EMAIL
        )

        self.db.session.delete(self.match)
        self.db.session.commit()

        match_one = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=30))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False,
                          home_current_score=0, away_current_score=0,
                          season=self.config.season(),
                          league=self.config.OPENLIGADB_LEAGUE)
        match_two = Match(home_team=self.team_two, away_team=self.team_one,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=120))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False,
                          home_current_score=0, away_current_score=0,
                          season=self.config.season(),
                          league=self.config.OPENLIGADB_LEAGUE)

        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.add(new_user)
        self.db.session.commit()

        self.assertEqual(reminder_one.get_due_matches(), [])
        self.assertEqual(reminder_two.get_due_matches(), [match_one])

        with self.context:
            with mock.patch("bundesliga_tippspiel.db.settings."
                            "ReminderSettings.send_email") as mocked:
                reminder_one.send_reminder()
                self.assertEqual(0, mocked.call_count)
                reminder_two.send_reminder()
                self.assertEqual(1, mocked.call_count)
                reminder_one.send_reminder()
                reminder_two.send_reminder()
                self.assertEqual(1, mocked.call_count)

        self.assertEqual(reminder_one.get_due_matches(), [])
        self.assertEqual(reminder_two.get_due_matches(), [])

        reminder_one.set_reminder_time(10000)
        reminder_two.set_reminder_time(10000)

        self.assertEqual(reminder_two.get_due_matches(),
                         [match_one, match_two])
        self.assertEqual(reminder_two.get_due_matches(),
                         [match_one, match_two])

        with self.context:
            with mock.patch("bundesliga_tippspiel.db.settings."
                            "ReminderSettings.send_email") as mocked:
                reminder_one.send_reminder()
                self.assertEqual(1, mocked.call_count)
                reminder_two.send_reminder()
                self.assertEqual(2, mocked.call_count)
                reminder_one.send_reminder()
                reminder_two.send_reminder()
                self.assertEqual(2, mocked.call_count)

    def test_due_when_bets_placed(self):
        """
        Tests if the is_due method works correctly when bets are placed
        :return: None
        """
        now = datetime.utcnow()
        reminder = ReminderSettings(
            user=self.user_two,
            reminder_time=600,
            reminder_type=ReminderType.EMAIL
        )

        self.db.session.delete(self.match)
        self.db.session.commit()

        match_one = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=5))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False,
                          home_current_score=0, away_current_score=0,
                          season=self.config.season(),
                          league=self.config.OPENLIGADB_LEAGUE)
        match_two = Match(home_team=self.team_two, away_team=self.team_one,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=7))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False,
                          home_current_score=0, away_current_score=0,
                          season=self.config.season(),
                          league=self.config.OPENLIGADB_LEAGUE)

        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.commit()

        self.assertEqual(len(reminder.get_due_matches()), 2)

        self.generate_sample_bet(self.user_two, match_one)
        self.assertEqual(len(reminder.get_due_matches()), 1)

        self.generate_sample_bet(self.user_two, match_two)
        self.assertEqual(len(reminder.get_due_matches()), 0)

    def test_cascades(self):
        """
        Tests if cascade deletes work correctly
        :return: None
        """
        self.assertEqual(len(ReminderSettings.query.all()), 1)
        db.session.delete(self.reminder.user)
        self.assertEqual(len(ReminderSettings.query.all()), 0)
