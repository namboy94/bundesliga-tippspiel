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

import time
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestApiKey(_ModelTestFramework):
    """
    Tests the ApiKey SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = ApiKey

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            ApiKey(user=self.user_one),
            ApiKey(key_hash="A")
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.api_key),
            (2, ApiKey(user=self.user_two, key_hash="A"))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        # No unique stuff
        pass

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: ApiKey.query.filter_by(id=self.api_key.id).first(),
             self.api_key),
            (lambda: ApiKey.query.filter_by(
                user_id=self.api_key.user_id
            ).first(),
             self.api_key)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.api_key, [])
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.api_key.__json__(False)
        without_children.update({"user": self.api_key.user.__json__(True)})
        self.assertEqual(
            self.api_key.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.api_key)

    def test_expiration(self):
        """
        Tests if expiration of an API key is noticed correctly
        :return: None
        """
        self.assertFalse(self.api_key.has_expired())
        self.api_key.creation_time = time.time() - 3000000
        self.assertTrue(self.api_key.has_expired())

    def test_automatic_timestamp(self):
        """
        Tests if the current time is correctly used as a default parameter
        for the creation timestamp
        :return: None
        """
        key = self.generate_sample_api_key(self.user_two)
        self.assertLess(time.time() - key.creation_time, 2)
        time.sleep(3)
        key = self.generate_sample_api_key(self.user_two)
        self.assertLess(time.time() - key.creation_time, 2)

    def test_verification(self):
        """
        Tests verifying an API key
        :return: None
        """
        key = "apikey"
        self.assertFalse(self.api_key.verify_key(key))
        self.assertFalse(
            self.api_key.verify_key("{}{}".format(self.api_key.id, key))
        )
        self.assertTrue(
            self.api_key.verify_key("{}:{}".format(self.api_key.id, key))
        )
        self.assertFalse(
            self.api_key.verify_key("{}:{}".format(self.api_key.id + 1, key))
        )
