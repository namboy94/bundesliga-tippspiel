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

import time
from jerrycan.base import db
from bundesliga_tippspiel.db.user_generated.ChatMessage import ChatMessage
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.db.ModelTestFramework import \
    _ModelTestFramework


class TestChatMessage(_ModelTestFramework):
    """
    Tests the ChatMessage SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.message = ChatMessage(user=self.user_one, text="ABC")
        db.session.add(self.message)
        db.session.commit()
        self.model_cls = ChatMessage

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            ChatMessage()
        ])

    def test_retrieving_from_db(self):
        """
        Tests retrieving model objects from the database
        :return: None
        """
        self._test_retrieving_from_db([
            (lambda: ChatMessage.query.filter_by(id=self.message.id).first(),
             self.message),
            (lambda: ChatMessage.query.filter_by(user=self.user_one).first(),
             self.message)
        ])

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        # TODO Add child and parent relations
        without_children = self.message.__json__(False)
        without_children.update({
            "user": self.message.user.__json__(True, ["chat_messages"]),
            "children": [],
            "parent": None
        })
        self.assertEqual(
            self.message.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.message)

    def test_using_chat(self):
        """
        Test typical interactions with the chat systems
        :return: None
        """
        parent = ChatMessage(user=self.user_one, text="ABC")
        db.session.add(parent)
        db.session.commit()

        child1 = ChatMessage(user=self.user_two, text="XYZ", parent=parent)
        db.session.add(child1)
        db.session.commit()

        child2 = ChatMessage(user=self.user_one, text="DEF", parent=child1)
        db.session.add(child2)
        db.session.commit()

        child3 = ChatMessage(user=self.user_one, text="GHI", parent=parent)
        db.session.add(child3)
        db.session.commit()

        self.assertEqual(parent.children, [child1, child3])
        self.assertEqual(parent.children[0].children[0], child2)
        self.assertEqual(child2.parent, child1)
        self.assertEqual(child1.parent, child3.parent)
        self.assertAlmostEqual(
            int(child1.creation_time), int(child1.last_edit)
        )

        time.sleep(2)

        child1.edit("LALA")
        db.session.commit()
        self.assertEqual(child1.get_text(), "LALA")
        self.assertTrue(child1.edited)
        self.assertLess(child1.creation_time, child1.last_edit)

        child1.delete()
        db.session.commit()
        self.assertEqual(child2.parent.parent, parent)
        self.assertIsNone(child1.get_text())
        self.assertEqual(child1.text, "")
