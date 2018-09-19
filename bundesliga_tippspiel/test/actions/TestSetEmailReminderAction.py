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
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder
from bundesliga_tippspiel.actions.SetEmailReminderAction import \
    SetEmailReminderAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestSetEmailReminderAction(_ActionTestFramework):
    """
    Class that tests the SetEmailReminder action
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        generated = self.generate_sample_user(True)
        self.user = generated["user"]  # type: User
        self.pw = generated["pass"]
        self.login_user(self.user)

    def generate_action(self) -> SetEmailReminderAction:
        """
        Generates a valid SetEmailReminderAction object
        :return: The generated SetEmailReminderAction
        """
        return SetEmailReminderAction(hours=24, active=True)

    def test_setting_updating_and_deleting_reminder(self):
        """
        Tests setting a reminder, updating it and deleting it afterwards
        :return: None
        """
        reminder = EmailReminder(
            id=1, user_id=self.user.id,
            last_reminder="1970-01-01:01-01-01",
            reminder_time=24 * 60 * 60
        )
        with self.context:
            self.assertEqual(EmailReminder.query.all(), [])
            self.action.execute()
            self.assertEqual(EmailReminder.query.all(), [reminder])

            self.action.hours = 48
            reminder.reminder_time = 48 * 60 * 60
            self.action.execute()
            self.assertEqual(EmailReminder.query.all(), [reminder])

            self.action.active = False
            self.action.execute()
            self.assertEqual(EmailReminder.query.all(), [])

            self.action.execute()
            self.assertEqual(EmailReminder.query.all(), [])

    def test_setting_invalid_reminder_times(self):
        """
        Tests setting a reminder time that's not 0 < t < 49
        :return: None
        """
        with self.context:
            for invalid in [-1, 0, 49]:
                self.action.hours = invalid
                self.failed_execute("invalid reminder hours")
                self.assertEqual(EmailReminder.query.all(), [])

            self.action.hours = 24
            self.action.execute()
            reminder = EmailReminder.query.first()

            for invalid in [-1, 0, 49]:
                self.action.hours = invalid
                self.failed_execute("invalid reminder hours")
                self.assertEqual(EmailReminder.query.all(), [reminder])
