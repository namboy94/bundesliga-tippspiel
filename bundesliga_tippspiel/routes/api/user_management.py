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

from flask import request
from bundesliga_tippspiel import app
from bundesliga_tippspiel.utils.routes import api
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction
from bundesliga_tippspiel.actions.ConfirmAction import ConfirmAction


@app.route("/api/v2/register", methods=["POST"])
@api
def api_register():
    """
    Allows registering a user using the API
    :return: The JSON response
    """
    action = RegisterAction.from_dict(request.get_json())
    return action.execute()
