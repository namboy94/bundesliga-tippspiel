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
from flask import jsonify, make_response, request
from werkzeug.exceptions import Unauthorized
from bundesliga_tippspiel.types.exceptions import ActionException


def api(func: Callable) -> Callable:
    """
    Decorator that handles common API patterns and ensures that
    the JSON response will always follow a certain pattern
    :param func: The function to wrap
    :return: The wrapper function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Tries running the function and checks for errors
        :param args: args
        :param kwargs: kwargs
        :return: The JSON response including an appropriate HTTP status code
        """
        code = 200
        response = {"status": "ok"}

        try:
            if request.method in ["POST", "PUT"] and \
                    (not request.content_type.startswith("application/json")
                     or not request.is_json
                     or not isinstance(request.get_json(silent=True), dict)):
                raise ActionException(
                    "Not in JSON format", "Not in JSON format"
                )

            response["data"] = func(*args, **kwargs)

        except (KeyError, TypeError, ValueError, ActionException) as e:

            response["status"] = "error"

            if isinstance(e, ActionException):
                code = e.status_code
                response["reason"] = e.reason

            else:  # pragma: no cover
                code = 400
                response["reason"] = "Bad Request"

        return make_response(jsonify(response), code)

    return wrapper


def api_login_required(func: Callable) -> Callable:
    """
    Decorator to make unauthorized API calls respond with JSON properly
    :param func: The function to wrap
    :return: The wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Checks if flask-login throws an Unauthorized exception. If so,
        re-wrap the response in JSON
        :param args: The function arguments
        :param kwargs: The function keyword arguments
        :return: The newly wrapped response,
                 or just the plain response if authorized
        """

        try:
            resp = func(*args, **kwargs)
            return resp
        except Unauthorized:
            return make_response(
                jsonify({"status": "error", "reason": "Unauthorized"}), 401
            )

    return wrapper


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
