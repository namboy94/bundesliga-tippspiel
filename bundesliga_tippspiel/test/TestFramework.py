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
import bundesliga_tippspiel.globals as glob
from unittest import TestCase


class TestFramework(TestCase):
    """
    Class that models a testing framework for the flask application
    """

    def setUp(self):
        """
        Sets up the SQLite database
        :return: None
        """
        glob.app.config["TESTING"] = True
        self.cleanup()
        self.app = glob.app
        self.db = glob.db
        glob.initialize_db("sqlite:////tmp/test.db")
        self.app.app_context().push()

    def tearDown(self):
        """
        Deletes the test database if it exists
        :return: None
        """
        self.cleanup()

    @staticmethod
    def cleanup():
        """
        Deletes the SQLite database file
        :return: None
        """
        try:
            os.remove("/tmp/test.db")
        except FileNotFoundError:
            pass
