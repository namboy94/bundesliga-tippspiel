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
        self.incomplete_columns = [
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
        ]
        self.indexed = [
            (1, self.team_one),
            (2, self.team_two),
            (3, Team(name="1", short_name="2", abbreviation="3",
                     icon_png="4", icon_svg="5"))
        ]
        self.non_uniques = [
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
        ]  # No unique attributes
