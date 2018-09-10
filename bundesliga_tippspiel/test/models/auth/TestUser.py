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
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestUser(_ModelTestFramework):
    """
    Tests the User SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = User

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            User(username="A", email="B", confirmation_hash="D"),
            User(username="A", password_hash="C", confirmation_hash="D"),
            User(email="B", password_hash="C", confirmation_hash="D"),
            User(username="A", email="B", password_hash="C")
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.user_one),
            (2, self.user_two),
            (3, User(
                username="A",
                email="B",
                password_hash="C",
                confirmation_hash="D"
            )),
            (4, User(
                username="E",
                email="F",
                password_hash="G",
                confirmation_hash="H"
            ))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            User(
                username=self.user_one.username,
                email="B",
                password_hash="C",
                confirmation_hash="D"
            ),
            User(
                username="A",
                email=self.user_one.email,
                password_hash="C",
                confirmation_hash="D"
            )
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: User.query.filter_by(id=self.user_one.id).first(),
             self.user_one),
            (lambda: User.query.filter_by(email=self.user_one.email).first(),
             self.user_one),
            (lambda: User.query.filter_by(
                username=self.user_two.username
            ).first(),
             self.user_two)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        self._test_deleting_from_db([
            (self.user_one, [self.api_key, self.reminder]),
            (self.user_two, [])
        ])

    def test_verifying_password(self):
        """
        Tests using the verify_password method
        :return: None
        """
        self.assertTrue(self.user_one.verify_password("samplepass1"))
        self.assertFalse(self.user_one.verify_password("samplepass2"))

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        self.assertEqual(
            self.user_one.__json__(True),
            self.user_one.__json__(False)
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.user_one)
