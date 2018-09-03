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
from bundesliga_tippspiel.actions.ApiKeyGenAction import ApiKeyGenAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework


class TestApiKeyGenAction(_ActionTestFramework):
    """
    Class that tests the ApiKeyGen action
    """

    def setUp(self):
        """
        Sets up users for testing
        :return: None
        """
        super().setUp()
        generated_users = self.generate_sample_users()
        self.confirmed_user = generated_users[0]["user"]  # type: User
        self.confirmed_user_pw = generated_users[0]["pass"]
        self.unconfirmed_user = generated_users[1]["user"]  # type: User
        self.unconfirmed_user_pw = generated_users[1]["pass"]

    def generate_action(self) -> ApiKeyGenAction:
        """
        Generates a valid ApiKeyGenAction object
        :return: The generated ApiKeyGenAction
        """
        return ApiKeyGenAction(
            username=self.confirmed_user.username,
            password=self.confirmed_user_pw
        )

    def test_invalid_user(self):
        """
        Tests using an invalid user
        :return: None
        """
        self.action.username = "NotExisting"
        self.failed_execute("User does not exist")

    def test_unconfirmed_user(self):
        """
        Tests that generating an API key is impossible for unconfirmed users
        :return: None
        """
        self.action.username = self.unconfirmed_user.username
        self.action.password = self.unconfirmed_user_pw
        self.failed_execute("User is not confirmed")

    def test_using_invalid_password(self):
        """
        Tests using an invalid password
        :return: None
        """
        self.action.password = "AAA"
        self.failed_execute("Invalid Password")

    def test_generating_api_keys(self):
        """
        Tests generating API keys. Two, for good measure.
        :return: None
        """
        first = self.action.execute()
        second = self.action.execute()

        self.assertNotEqual(first["api_key"], second["api_key"])

        for key_data in [first, second]:

            key = ApiKey.query.get(key_data["api_key"].split(":")[0])
            self.assertEqual(
                int(key.creation_time) + ApiKey.MAX_AGE,
                key_data["expiration"]
            )
            self.assertTrue(key.verify_key(key_data["api_key"]))
