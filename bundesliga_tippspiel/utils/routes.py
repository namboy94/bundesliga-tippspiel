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

from flask import abort
from functools import wraps
from typing import Callable
from bundesliga_tippspiel.exceptions import ActionException


def action_route(func: Callable) -> Callable:
    """
    Decorator that catches any ActionExceptions and displays appropriate
    error messages
    :param func: The function to wrap
    :return: The wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Checks if an ActionException occurred and aborts using the
        correct status code
        :param args: The function arguments
        :param kwargs: The function keyword arguments
        :return: The newly wrapped response,
                 or just the plain response if authorized
        """

        try:
            resp = func(*args, **kwargs)
            return resp
        except ActionException as e:
            abort(e.status_code)

    return wrapper
