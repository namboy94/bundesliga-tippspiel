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
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestEmailReminder(_ModelTestFramework):
    """
    Tests the EmailReminder SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = EmailReminder

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            EmailReminder(user=self.user_two),
            EmailReminder(reminder_time=1)
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.reminder),
            (2, EmailReminder(user=self.user_two, reminder_time=2))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            EmailReminder(user=self.user_one, reminder_time=2)
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: EmailReminder.query.filter_by(
                id=self.reminder.id).first(),
             self.reminder)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.reminder, [])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.reminder.__json__(False)
        without_children.update({
            "user": self.reminder.user.__json__(True)
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
        reminder_one = EmailReminder(user=self.user_two, reminder_time=600)
        reminder_two = EmailReminder(user=new_user, reminder_time=3600)

        match_one = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=30))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False)
        match_two = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=120))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False)

        self.db.session.delete(self.match)
        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.add(new_user)
        self.db.session.commit()

        self.assertEqual(reminder_one.get_due_matches(), [])
        self.assertEqual(reminder_two.get_due_matches(), [match_one])

        with self.context:
            with mock.patch("bundesliga_tippspiel.models.user_generated."
                            "EmailReminder.send_email") as mocked:
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
            with mock.patch("bundesliga_tippspiel.models.user_generated."
                            "EmailReminder.send_email") as mocked:
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
        reminder = EmailReminder(user=self.user_two, reminder_time=600)

        match_one = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=5))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False)
        match_two = Match(home_team=self.team_one, away_team=self.team_two,
                          matchday=1,
                          kickoff=(now + timedelta(minutes=7))
                          .strftime("%Y-%m-%d:%H-%M-%S"),
                          started=False, finished=False)

        self.db.session.delete(self.match)
        self.db.session.add(match_one)
        self.db.session.add(match_two)
        self.db.session.commit()

        self.assertEqual(len(reminder.get_due_matches()), 2)

        self.generate_sample_bet(self.user_two, match_one)
        self.assertEqual(len(reminder.get_due_matches()), 1)

        self.generate_sample_bet(self.user_two, match_two)
        self.assertEqual(len(reminder.get_due_matches()), 0)
