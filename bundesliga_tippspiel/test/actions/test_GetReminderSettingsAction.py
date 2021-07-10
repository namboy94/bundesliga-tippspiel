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
from bundesliga_tippspiel.actions.GetReminderSettingsAction import \
    GetReminderSettingsAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestGetReminderSettingsAction(_ActionTestFramework):
    """
    Class that tests the GetReminderSettingsAction action
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        self.user, self.password, _ = self.generate_sample_user(True)
        self.login_user(self.user, self.password, False)
        self.reminder = ReminderSettings(
            id=1, user_id=self.user.id,
            reminder_type=ReminderType.EMAIL,
            last_reminder="1970-01-01:01-01-01",
            reminder_time=24 * 60 * 60
        )
        self.db.session.add(self.reminder)
        self.db.session.commit()

    def generate_action(self) -> GetReminderSettingsAction:
        """
        Generates a valid SetReminderSettingsAction object
        :return: The generated SetReminderSettingsAction
        """
        return GetReminderSettingsAction()

    def test_setting_updating_and_deleting_reminder(self):
        """
        Tests getting a reminder
        :return: None
        """
        with self.context:
            resp = self.action.execute()
            self.assertEqual(
                resp["settings"][ReminderType.EMAIL],
                self.reminder
            )

            self.db.session.delete(self.reminder)
            self.db.session.commit()

            resp = self.action.execute()
            self.assertEqual(
                resp["settings"][ReminderType.EMAIL],
                None
            )

    def test_from_dict(self):
        """
        Tests the from_dict method
        :return: None
        """
        GetReminderSettingsAction.from_dict({})
