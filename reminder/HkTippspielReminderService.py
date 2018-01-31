#!/usr/bin/env python
"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

kudubot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kudubot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List
from kudubot.entities.Message import Message
from kudubot.services.BaseService import BaseService

class HkTippspielReminderService(BaseService):

    def init(self):
        self.initialize_database_table(initializer=)

    def is_applicable_to(self, message: Message) -> bool:
        pass

    @staticmethod
    def define_requirements() -> List[str]:
        pass

    def handle_message(self, message: Message):
        pass

    @staticmethod
    def define_identifier() -> str:
        pass