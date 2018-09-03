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

import json
from base64 import b64encode
from flask import Response
from typing import Tuple, List, Dict, Any, Optional
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class _ApiRouteTestFramework(_TestFramework):
    """
    Framework for testing API routes
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        self.user = User(
            username="RouteUser",
            email="route@hk-tippspiel.com",
            password_hash="$2b$12$xwI3.FxhPmL3EeAgJICetO12AzB"
                          "vEdlBY8bQ1HZtcIjULkZg3/Kb2",
            confirmation_hash="",
            confirmed=True
        )
        self.db.session.add(self.user)
        self.db.session.commit()
        self.pw = "route"
        self.api_key = "RouteApiKey"
        self.api_key_obj = ApiKey(
            user=self.user,
            key_hash="$2b$12$zsSlceHzC.U8syusgrWIW."
                     "1ntT10TjFeViYNkikzRp3u5yzfYNnxO"
        )
        self.db.session.add(self.api_key_obj)
        self.db.session.commit()
        self.api_key = "{}:{}".format(self.api_key_obj.id, self.api_key)

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        raise NotImplementedError()

    @property
    def route_path(self) -> str:
        """
        :return: The API path
        """
        return self.route_info[0]

    @property
    def methods(self) -> List[str]:
        """
        :return: The methods the API endpoint supports
        """
        return self.route_info[1]

    @property
    def auth_required(self) -> bool:
        """
        :return: Whether or not authentication is required for this route
        """
        return self.route_info[2]

    def test_content_type(self):
        """
        Tests that an incorrect content type in the request
        is successfully handled
        :return: None
        """
        headers = self.generate_headers() if self.auth_required else {}

        for method in self.route_info[1]:
            if method not in ["POST", "PUT"]:
                continue

            for data, content_type in [
                ({}, "text/html"),
                (None, "application/json"),
                ("", "application/json")
            ]:
                if method == "POST":
                    resp = self.client.post(
                        self.route_info[0],
                        json=data,
                        content_type=content_type,
                        headers=headers
                    )
                else:  # == PUT
                    resp = self.client.put(
                        self.route_info[0],
                        json=data,
                        content_type=content_type,
                        headers=headers
                    )

                self.assertEqual(resp.status_code, 400)
                data = self.decode_data(resp)
                self.assertEqual(data["status"], "error")
                self.assertEqual(data["reason"], "Not in JSON format")

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        raise NotImplementedError()

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        raise NotImplementedError()

    @staticmethod
    def decode_data(response: Response) -> Dict[str, Any]:
        """
        Decodes the response's data
        :return: The JSON data
        """
        return json.loads(response.data.decode("utf-8"))

    def generate_headers(self, api_key: Optional[str] = None) \
            -> Dict[str, str]:
        """
        Generates base64 encoded authorization headers for an API key
        :param api_key: The API key to use. Of not provided,
                        will use self.api_key
        :return: The headers
        """
        if api_key is None:
            api_key = self.api_key

        encoded = b64encode(api_key.encode("utf-8")).decode("utf-8")
        return {
            "Authorization": "Basic {}".format(encoded)
        }
