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


class TestStaticRoutes(_TestFramework):
    """
    Class that tests the routes defined by static routes
    """

    def test_index(self):
        """
        Tests the index page
        :return: None
        """
        resp = self.client.get("/")
        self.assertTrue(
            b"Tippspiel zur Bundesliga Saison 2018/19" in resp.data
        )

    def test_about(self):
        """
        Tests the about/impressum page
        :return: None
        """
        resp = self.client.get("/about")
        self.assertTrue(b"eRecht24" in resp.data)

    def test_privacy(self):
        """
        Tests the privacy statement page
        :return: None
        """
        resp = self.client.get("/privacy")
        self.assertTrue(
            b"Erstellt mit Datenschutz-Generator.de von RA Dr. Thomas Schwenke"
            in resp.data
        )
