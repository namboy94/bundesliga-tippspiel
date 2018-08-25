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

# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.utils.crypto import generate_hash, generate_random, \
    verify_password


class TestCrypto(_TestFramework):
    """
    Tests cryptographical functions
    """

    def test_hashing(self):
        """
        Tests that passwords can be hashed successfully
        :return: None
        """
        password_one = generate_random(30)
        password_two = generate_random(20)

        hash_one = generate_hash(password_one)
        hash_two = generate_hash(password_two)

        self.assertEqual(len(hash_one), len(hash_two))
        self.assertNotEqual(hash_one, hash_two)

        self.assertTrue(verify_password(password_one, hash_one))
        self.assertTrue(verify_password(password_two, hash_two))
        self.assertFalse(verify_password(password_one, hash_two))
        self.assertFalse(verify_password(password_two, hash_one))

    def test_salt(self):
        """
        Tests that password hashes are salted
        :return: None
        """
        password = generate_random(30)
        hash_one = generate_hash(password)
        hash_two = generate_hash(password)

        self.assertNotEqual(hash_one, hash_two)

        self.assertTrue(verify_password(password, hash_one))
        self.assertTrue(verify_password(password, hash_two))

    def test_hashing_strings(self):
        """
        Tests that password hashing and verifying works with string as well
        :return: None
        """
        password = str(generate_random(30))
        _hash = generate_hash(password)
        self.assertTrue(verify_password(password, _hash.decode("utf-8")))

    def test_verifying_with_invalid_hash(self):
        """
        Tests that attempting to verify a password with an incorrectly
        formatted hash will return False
        :return: None
        """
        self.assertFalse(verify_password("A", "A"))
