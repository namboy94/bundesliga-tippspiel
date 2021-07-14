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

from jerrycan.base import db
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.db.ModelTestFramework import \
    _ModelTestFramework
from bundesliga_tippspiel.db.match_data.Player import Player


class TestPlayer(_ModelTestFramework):
    """
    Tests the Player SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = Player

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            Player(team=self.team_one),
            Player(name="1")
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: Player.query.filter_by(
                name=self.player.name,
                team_abbreviation=self.player.team_abbreviation
            ).first(),
             self.player)
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.player.__json__(False)
        without_children.update({
            "team": self.player.team.__json__(True, ["players", "player"]),
            "goals": [x.__json__(True, ["player"]) for x in self.player.goals]
        })
        self.assertEqual(
            self.player.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.player)

    def test_cascades(self):
        """
        Tests if cascade deletes work correctly
        :return: None
        """
        self.assertEqual(len(Player.query.all()), 1)
        db.session.delete(self.goal)
        self.assertEqual(len(Player.query.all()), 1)
        db.session.delete(self.player.team)
        self.assertEqual(len(Player.query.all()), 0)
