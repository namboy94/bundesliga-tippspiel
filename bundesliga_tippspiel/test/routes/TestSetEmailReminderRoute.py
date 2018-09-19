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

from typing import Tuple, Optional, List
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestSetEmailReminderRoute(_RouteTestFramework):
    """
    Class that tests the /set_email_reminder route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], Optional[str], bool]:
        """
        Info about the route to test
        :return: The route's path,
                 the route's primary methods,
                 A phrase found on the route's GET page.
                 None if no such page exists,
                 An indicator for if the page requires authentication or not
        """
        return "/set_email_reminder", ["POST"], None, True

    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        self.assertEqual(len(EmailReminder.query.all()), 0)
        self.login()
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            "hours": 10,
            "active": "on"
        })
        self.assertTrue(b"Erinnerungsdaten gespeichert" in resp.data)
        self.assertEqual(len(EmailReminder.query.all()), 1)

    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        self.assertEqual(len(EmailReminder.query.all()), 0)
        self.login()
        resp = self.client.post(self.route_path, follow_redirects=True, data={
            "hours": 100,
            "active": True
        })
        self.assertTrue(b"Anzahl Stunden eingegeben" in resp.data)
        self.assertEqual(len(EmailReminder.query.all()), 0)
