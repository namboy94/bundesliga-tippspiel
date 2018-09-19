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

from typing import Dict, Any
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.actions.GetEmailReminderAction import \
    GetEmailReminderAction
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.GetterApiRouteTestFramework import \
    _GetterApiRouteTestFramework


class TestGetEmailReminderApiRoute(_GetterApiRouteTestFramework):
    """
    Tests the /email_reminder GET API route
    """

    @property
    def keyword(self) -> str:
        """
        :return: The route keyword
        """
        return "email_reminder"

    @property
    def sample_filters(self) -> Dict[str, Any]:
        """
        :return: A sample dictionary of filters with appropriate values
        """
        return {}

    @property
    def action_cls(self) -> type(Action):
        """
        :return: The action class used to fetch data
        """
        return GetEmailReminderAction

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        resp = self.client.get(
            self.route_path, headers=self.generate_headers()
        )
        self.assertEqual(
            self.decode_data(resp)["data"]["email_reminder"], None
        )

        reminder = EmailReminder(
            id=1, user_id=self.user.id,
            last_reminder="1970-01-01:01-01-01",
            reminder_time=24 * 60 * 60
        )
        self.db.session.add(reminder)
        self.db.session.commit()

        resp = self.client.get(
            self.route_path, headers=self.generate_headers()
        )
        self.assertEqual(
            self.decode_data(resp)["data"]["email_reminder"],
            reminder.__json__(True)
        )

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        pass
