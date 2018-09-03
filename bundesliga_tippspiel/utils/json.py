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


def jsonify_models(data: Dict[str, Any], deep: bool = True) -> Dict[str, Any]:
    """
    Serializes a dictionary and calls the __json__() method on all
    objects that have one.
    :param data: The data to serialize
    :param deep: Indicates whether or not child models are included.
                 If False, only IDs will be included.
    :return: The serialized data
    """
    to_jsonify = {}
    for key, val in data.items():
        to_jsonify[key] = _serialize(val, deep)
    return to_jsonify


def _serialize(obj: Any, deep: bool) -> Any:
    """
    Serializes an object, so that it can be jsonified without issues
    :param obj: The object to serialize
    :param deep: Indicates whether or not child models are included.
                 If False, only IDs will be included.
    :return: The serialized object
    """
    if isinstance(obj, dict):
        serialized = {}
        for key, val in obj.items():
            serialized[key] = _serialize(val, deep)
        return serialized

    elif isinstance(obj, list):
        serialized = []
        for val in obj:
            serialized.append(_serialize(val, deep))
        return serialized

    elif isinstance(obj, tuple):
        return tuple(_serialize(list(obj), deep))

    elif "__json__" in dir(obj):
        return obj.__json__(deep)
    else:
        return obj
