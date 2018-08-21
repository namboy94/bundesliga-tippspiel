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

from bundesliga_tippspiel.utils.db import username_exists
from bundesliga_tippspiel.config import smtp_address
from bundesliga_tippspiel.test.TestFramework import TestFramework


class TestRouter(TestFramework):
    """
    Class that tests the routes defined in router.py
    """

    def test_register(self):
        """
        Tests the /register route
        :return: None
        """
        get = self.client.get("/register")
        self.assertTrue(b"Registrierung" in get.data)

        self.assertFalse(username_exists("TestUser"))
        post = self.client.post("/register", follow_redirects=True, data={
            "username": "TestUser",
            "email": smtp_address,
            "password": "Abc",
            "password-repeat": "Abc",
            "g-recaptcha-response": ""
        })
        self.assertTrue(b"Siehe in deiner Email-Inbox nach" in post.data)
        self.assertTrue(username_exists("TestUser"))

        self.assertFalse(username_exists("TestUser2"))
        failed_post = self.client.post(
            "/register",
            follow_redirects=True,
            data={
                "username": "TestUser2",
                "email": "A" + smtp_address,
                "password": "Abc",
                "password-repeat": "AbC",
                "g-recaptcha-response": ""
            }
        )
        self.assertFalse(b"Siehe in deiner Email-Inbox" in failed_post.data)
        self.assertTrue(b"Die angegebenen Passw" in failed_post.data)
        self.assertFalse(username_exists("TestUser2"))