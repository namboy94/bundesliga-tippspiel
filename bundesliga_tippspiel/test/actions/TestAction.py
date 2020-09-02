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

from puffotter.flask.base import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class ActionTest(_TestFramework):
    """
    Class that tests the static helper functions of the Action class
    """

    def test_getting_current_matchday(self):
        """
        Tests getting the current matchday
        :return: None
        """
        self.assertEqual(Action.get_current_matchday(), 34)
        _, _, _, match, _ = self.generate_sample_match_data()
        self.assertEqual(Action.get_current_matchday(), 34)
        match.finished = False
        match.started = False
        db.session.commit()
        self.assertNotEqual(Action.get_current_matchday(), 34)
        self.assertEqual(Action.get_current_matchday(), match.matchday)
