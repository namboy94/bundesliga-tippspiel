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
from typing import List, Optional, Dict, Any
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.db.User import User


class ChatMessage(ModelMixin, db.Model):
    """
    Model that describes the 'chat_messages' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "chat_messages"

    id: int = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )
    parent_id: int = db.Column(
        db.Integer, db.ForeignKey("chat_messages.id"), nullable=True
    )

    text: str = db.Column(db.String(255), nullable=False)
    creation_time: float = db.Column(
        db.Float, nullable=False, default=time.time
    )
    last_edit: float = db.Column(db.Float, nullable=False, default=time.time)
    edited: bool = db.Column(db.Boolean, nullable=False, default=False)
    deleted: bool = db.Column(db.Boolean, nullable=False, default=False)

    user: Optional[User] = db.relationship(
        "User", backref=db.backref("chat_messages")
    )

    parent: "ChatMessage" = db.relationship(
        "ChatMessage",
        back_populates="children",
        remote_side=[id],
        uselist=False
    )
    children: List["ChatMessage"] = db.relationship(
        "ChatMessage", back_populates="parent", uselist=True
    )

    def get_text(self) -> Optional[str]:
        """
        :return: The text of the chat message if the user still exists and the
                 message has not been deleted
        """
        if self.deleted or self.user is None:
            return None
        else:
            return self.text

    def edit(self, new_text: str):
        """
        Edits the message
        :param new_text: The new message text
        :return: None
        """
        self.text = new_text
        self.edited = True
        self.last_edit = time.time()

    def delete(self):
        """
        Marks the message as deleted
        :return: None
        """
        self.text = ""
        self.deleted = True

    def __json__(
            self,
            include_children: bool = False,
            ignore_keys: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Makes sure to include children and parents
        :param include_children: Whether or not to include child objects
        :param ignore_keys: Which keys to ignore
        :return: The JSON data
        """
        data = super().__json__(include_children, ignore_keys)
        # TODO Add child and parent relations
        return data
