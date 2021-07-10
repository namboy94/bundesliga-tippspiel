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

from typing import List, Tuple, Callable
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework


class _ModelTestFramework(_TestFramework):
    """
    A framework for testing match data models
    """

    def setUp(self):
        """
        Sets up some sample data
        :return: None
        """
        super().setUp()
        self.model_cls = None  # type: db.Model
        self.team_one, self.team_two, self.player, self.match, self.goal = \
            self.generate_sample_match_data()

        self.user_one = self.generate_sample_user(True)[0]
        self.user_two = self.generate_sample_user(True)[0]
        self.api_key = self.generate_api_key(self.user_one)[0]
        self.bet = self.generate_sample_bet(self.user_one, self.match)
        self.reminder = ReminderSettings(
            user=self.user_one,
            reminder_type=ReminderType.EMAIL,
            reminder_time=1
        )
        self.db.session.add(self.reminder)
        self.db.session.commit()

    def _test_missing_column_data(
            self, incomplete_columns: List[db.Model]
    ):
        """
        Tests that missing column data is handled correctly
        :param incomplete_columns: A list of model objects
                                   with missing column data
        :return: None
        """
        for obj in incomplete_columns:
            self.__test_invalid_db_add(obj)

    def _test_uniqueness(self, non_uniques: List[db.Model]):
        """
        Tests that unique attributes are correctly checked
        :param non_uniques: A list of model objects containing
                            non-unique column data
        :return: None
        """
        for non_unique in non_uniques:
            self.__test_invalid_db_add(non_unique)

    def _test_retrieving_from_db(
            self, queries: List[Tuple[Callable, db.Model]]
    ):
        """
        Tests retrieving model objects from the database
        :param queries: A list of tuples containing queries and
                        their expected result
        :return: None
        """
        for query, result in queries:
            self.assertEqual(query(), result)

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

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        raise NotImplementedError()

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        raise NotImplementedError()

    def _test_string_representation(self, model: ModelMixin):
        """
        Tests the str and repr methods of a model
        Acts as a class-independent testing method
        :param model: The model object to test.
        :return: None
        """
        data = model.__json__()

        if "id" in data:
            _id = data.pop("id")
            self.assertEqual(
                str(model),
                "{}:{} <{}>".format(
                    model.__class__.__name__,
                    _id,
                    str(data)
                )
            )
        else:
            self.assertEqual(
                str(model),
                "{} <{}>".format(
                    model.__class__.__name__,
                    str(data)
                )
            )

        # noinspection PyUnresolvedReferences
        from jerrycan.db.ApiKey import ApiKey
        # noinspection PyUnresolvedReferences
        from jerrycan.db.User import User
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.match_data.Player import Player
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.match_data.Team import Team
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.match_data.Goal import Goal
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.match_data.Match import Match
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.user_generated.Bet import Bet
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.user_generated.SeasonWinner import \
            SeasonWinner
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.SeasonEvent import \
            SeasonEvent, SeasonEventType
        # noinspection PyUnresolvedReferences
        from bundesliga_tippspiel.db.user_generated.ChatMessage import \
            ChatMessage

        exec("self.assertEqual(model, {})".format(repr(model)))
