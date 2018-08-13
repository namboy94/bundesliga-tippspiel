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

from bundesliga_tippspiel.test.models.ModelTestFramework import \
    ModelTestFramework
from bundesliga_tippspiel.models.match_data.Team import Team


class TestTeam(ModelTestFramework):
    """
    Tests the Team SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Team

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Team(name="1", short_name="2", abbreviation="3",
                 icon_png="4"),
            Team(name="1", short_name="2", abbreviation="3",
                 icon_svg="5"),
            Team(name="1", short_name="2",
                 icon_png="4", icon_svg="5"),
            Team(name="1", abbreviation="3",
                 icon_png="4", icon_svg="5"),
            Team(short_name="2", abbreviation="3",
                 icon_png="4", icon_svg="5")
        ])

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        self._test_auto_increment([
            (1, self.team_one),
            (2, self.team_two),
            (3, Team(name="1", short_name="2", abbreviation="3",
                     icon_png="4", icon_svg="5"))
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            Team(name=self.team_one.name, short_name="2", abbreviation="3",
                 icon_png="4", icon_svg="5"),
            Team(name="1", short_name=self.team_one.short_name,
                 abbreviation="3", icon_png="4", icon_svg="5"),
            Team(name="1", short_name="2",
                 abbreviation=self.team_one.abbreviation,
                 icon_png="4", icon_svg="5"),
            Team(name="1", short_name="2", abbreviation="3",
                 icon_png=self.team_one.icon_png, icon_svg="5"),
            Team(name="1", short_name="2", abbreviation="3",
                 icon_png="4", icon_svg=self.team_one.icon_svg)
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Team.query.filter_by(id=self.team_one.id).first(),
             self.team_one),
            (lambda: Team.query.filter_by(name=self.team_two.name).first(),
             self.team_two)
        ])

    def test_deleting_from_db(self):
        """
        Tests deleting model objects from the database
        :return: None
        """
        # TODO Match not cascading correctly
        self._test_deleting_from_db([
            (self.team_one, [self.player])
        ])