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

from typing import Tuple, List
from unittest import mock
from bundesliga_tippspiel.config import smtp_address
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class TestForgotApiRoute(_ApiRouteTestFramework):
    """
    Tests the /forgot API route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/forgot", ["POST"], False

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        user = self.generate_sample_user(True)["user"]
        user.email = smtp_address
        self.db.session.commit()

        with mock.patch(
                "bundesliga_tippspiel.actions.ForgotPasswordAction.send_email",
                lambda x, y, z: self.assertEqual(x, smtp_address)
        ):
            resp = self.client.post(self.route_info[0], json={
                "email": smtp_address,
                "g-recaptcha-response": ""
            }, content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            resp_data = self.decode_data(resp)
            self.assertEqual(resp_data["data"], {})

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        resp = self.client.post(self.route_info[0], json={
            "email": smtp_address,
            "g-recaptcha-response": ""
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        resp_data = self.decode_data(resp)
        self.assertEqual(resp_data["reason"], "Email not registered")
