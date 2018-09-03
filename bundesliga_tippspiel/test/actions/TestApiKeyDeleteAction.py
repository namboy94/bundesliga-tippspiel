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

from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.ApiKeyDeleteAction import ApiKeyDeleteAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestApiKeyDeleteAction(_ActionTestFramework):
    """
    Class that tests the ApiKeyDelete action
    """

    def setUp(self):
        """
        Sets up users for testing
        :return: None
        """
        super().setUp()
        generated_users = self.generate_sample_users()
        self.user = generated_users[0]["user"]  # type: User
        self.user_pw = generated_users[0]["pass"]
        self.api_key = self.generate_sample_api_key(self.user)

    def generate_action(self) -> ApiKeyDeleteAction:
        """
        Generates a valid ApiKeyDeleteAction object
        :return: The generated ApiKeyDeleteAction
        """
        return ApiKeyDeleteAction(
            api_key="{}:{}".format(self.api_key.id, self.API_KEY)
        )

    def test_non_existant_api_key(self):
        """
        Tests using a non-existant API key
        :return: None
        """
        for key in [
            "adagsfsad",
            "100:{}".format(self.API_KEY)
        ]:
            self.action.api_key = key
            self.failed_execute("API Key does not exist")

        self.action.api_key = "{}:{}".format(self.api_key.id, "AAAAA")
        self.failed_execute("API key not valid")

    def test_deleting_api_key(self):
        """
        Tests deleting an API key
        :return: None
        """
        self.assertIsNotNone(ApiKey.query.get(self.api_key.id))
        self.action.execute()
        self.assertIsNone(ApiKey.query.get(self.api_key.id))
