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

import os
from unittest import TestCase
from bundesliga_tippspiel.config import resolve_env_variable


class TestEnv(TestCase):
    """
    Unit test class that tests environment variable functions
    """

    def test_resolving_env_variable(self):
        """
        Tests resolving environment variables
        :return: None
        """
        self.assertTrue("SMTP_PASSWORD" in os.environ)
        smtp_password = resolve_env_variable("SMTP_PASSWORD", str)
        self.assertEqual(smtp_password, os.environ["SMTP_PASSWORD"])

        not_existing = resolve_env_variable("NOT_EXISTING", str, "A")
        self.assertEqual(not_existing, "A")

        db_var = resolve_env_variable("DB_VAR", str)
        self.assertEqual(db_var, None)

        try:
            resolve_env_variable("NOT_EXISTING", str)
            self.fail()
        except KeyError as e:
            self.assertEqual(str(e), "'NOT_EXISTING'")
