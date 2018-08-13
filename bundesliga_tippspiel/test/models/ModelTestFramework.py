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

from typing import List, Tuple
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from bundesliga_tippspiel.globals import db
from bundesliga_tippspiel.test.TestFramework import TestFramework


class ModelTestFramework(TestFramework):
    """
    A framework for testing match data models
    """

    def setUp(self):
        """
        Sets up some sample data
        :return: None
        """
        super().setUp()
        self.team_one, self.team_two, self.player, self.match, self.goal = \
            self.generate_sample_match_data()
        self.incomplete_columns = []  # type: List[self.db.Model]
        self.index_map = []  # type: List[Tuple[int, self.db.Model]]
        self.non_uniques = []  # type: List[self.db.Model]

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        for obj in self.incomplete_columns:
            self.__test_invalid_db_add(obj)

    def test_auto_increment(self):
        """
        Tests that auto-incrementing works as expected
        :return: None
        """
        for index, obj in self.index_map:

            if obj.id is None:
                self.db.session.add(obj)
                self.db.session.commit()

            self.assertEqual(obj.id, index)

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        for non_unique in self.non_uniques:
            self.__test_invalid_db_add(non_unique)

    def __test_invalid_db_add(self, obj: db.Model):
        """
        Tests adding a database model object to the database and makes sure
        it fails.
        :param obj: The object to add
        :return: None
        """
        self.db.session.add(obj)
        try:
            self.db.session.commit()
            self.fail()
        except (IntegrityError, FlushError):
            self.db.session.rollback()
