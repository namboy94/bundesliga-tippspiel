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

from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings
from bundesliga_tippspiel.actions.SetReminderSettingsAction import \
    SetReminderSettingsAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestSetReminderSettingsAction(_ActionTestFramework):
    """
    Class that tests the SetReminderSettings action
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        self.user, self.pw, _ = self.generate_sample_user(True)
        self.login_user(self.user, self.pw, False)

    def generate_action(self) -> SetReminderSettingsAction:
        """
        Generates a valid SetReminderSettingsAction object
        :return: The generated SetReminderSettingsAction
        """
        return SetReminderSettingsAction(
            hours=24, reminder_states={ReminderType.EMAIL: True}
        )

    def test_setting_and_updating_reminder(self):
        """
        Tests setting a reminder and updating it
        :return: None
        """
        reminder = ReminderSettings(
            id=1, user_id=self.user.id, active=True,
            reminder_type=ReminderType.EMAIL,
            last_reminder="1970-01-01:01-01-01",
            reminder_time=24 * 60 * 60
        )
        with self.context:
            self.assertEqual(ReminderSettings.query.all(), [])
            self.action.execute()
            self.assertEqual(ReminderSettings.query.all(), [reminder])

            self.action.hours = 48
            reminder.reminder_time = 48 * 60 * 60
            self.action.execute()
            self.assertEqual(ReminderSettings.query.all(), [reminder])

    def test_setting_invalid_reminder_times(self):
        """
        Tests setting a reminder time that's not 0 < t < 49
        :return: None
        """
        with self.context:
            for invalid in [-1, 0, 49]:
                self.action.hours = invalid
                self.failed_execute("invalid reminder hours")
                self.assertEqual(ReminderSettings.query.all(), [])

            self.action.hours = 24
            self.action.execute()
            reminder = ReminderSettings.query.first()

            for invalid in [-1, 0, 49]:
                self.action.hours = invalid
                self.failed_execute("invalid reminder hours")
                self.assertEqual(ReminderSettings.query.all(), [reminder])
