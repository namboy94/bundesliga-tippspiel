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

from typing import Dict, Any
from bundesliga_tippspiel import db


class ModelMixin:
    """
    A mixin class that specifies a couple of methods all database
    models should implement
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
    """

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        raise NotImplementedError()  # pragma: no cover

    def __str__(self) -> str:
        """
        :return: The string representation of this object
        """
        data = self.__json__()
        _id = data.pop("id")
        return "{}:{} <{}>".format(self.__class__.__name__, _id, str(data))

    def __repr__(self) -> str:
        """
        :return: A string with which the object may be generated
        """
        params = ""

        for key, val in self.__json__().items():
            params += "{}={}, ".format(key, repr(val))
        params = params.rsplit(",", 1)[0]

        return "{}({})".format(self.__class__.__name__, params)

    def __eq__(self, other: Any) -> bool:
        """
        Checks the model object for equality with another object
        :param other: The other object
        :return: True if the objects are equal, False otherwise
        """
        if "__json__" in dir(other):
            return other.__json__() == self.__json__()
        else:
            return False  # pragma: no cover
