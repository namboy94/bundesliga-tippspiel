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
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder
from bundesliga_tippspiel.actions.SendDueEmailRemindersAction import \
    SendDueEmailRemindersAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestSetEmailReminderAction(_ActionTestFramework):
    """
    Class that tests the SendDueEmailRemindersAction action
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        generated = self.generate_sample_user(True)

        now = datetime.utcnow()
        now_str = now.strftime("%Y-%m-%d:%H-%M-%S")
        then = now + timedelta(hours=24)
        then_str = then.strftime("%Y-%m-%d:%H-%M-%S")

        self.user = generated["user"]  # type: User
        self.reminder = EmailReminder(
            id=1, user_id=self.user.id,
            last_reminder=now_str,
            reminder_time=48 * 60 * 60
        )
        _, _, _, self.match, _ = self.generate_sample_match_data()
        self.match.kickoff = then_str
        self.db.session.add(self.reminder)
        self.db.session.commit()

    def generate_action(self) -> SendDueEmailRemindersAction:
        """
        Generates a valid SendDueEmailRemindersAction object
        :return: The generated SendDueEmailRemindersAction
        """
        return SendDueEmailRemindersAction()

    def test_without_stored_reminders(self):
        """
        Tests running the action without any stored reminders
        :return: None
        """
        self.db.session.delete(self.reminder)
        self.db.session.commit()
        with mock.patch("bundesliga_tippspiel.models.user_generated."
                        "EmailReminder.send_email") as mocked:
            self.action.execute()
            self.assertEqual(0, mocked.call_count)

    def test_with_non_due_reminder(self):
        """
        Tests running the action with a reminder that's not due yet
        :return: None
        """
        self.reminder.last_reminder = self.match.kickoff
        self.db.session.commit()
        with mock.patch("bundesliga_tippspiel.models.user_generated."
                        "EmailReminder.send_email") as mocked:
            self.action.execute()
            self.assertEqual(0, mocked.call_count)

    def test_with_due_reminder(self):
        """
        Tests running the action with a due reminder
        :return: None
        """
        with self.context:
            with mock.patch("bundesliga_tippspiel.models.user_generated."
                            "EmailReminder.send_email") as mocked:
                self.action.execute()
                self.assertEqual(1, mocked.call_count)
                self.action.execute()
                self.assertEqual(1, mocked.call_count)

    def test_from_dict(self):
        """
        "Tests" the from_dict method
        :return: None
        """
        SendDueEmailRemindersAction.from_dict({})
