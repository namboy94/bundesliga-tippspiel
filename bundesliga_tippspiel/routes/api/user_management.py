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

from flask import make_response, request, jsonify
from bundesliga_tippspiel import app
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction


@app.route("/api/v2/register", methods=["POST"])
def api_register():
    """
    Enables registering a user using the API
    :return: None
    """
    json_data = request.get_json()
    action = RegisterAction.from_site_request()

    code = 200

    try:
        action.execute()
    except ActionException as e:


    resp_data = {}
    resp = {"status": "ok", "data": resp_data}

    return make_response(jsonify(resp), code)


# How API works:

# REQUEST
#   Not Auth'ed:
#       {key: val}
#   Auth'ed:
#       {"api_key": "user_id:key", key: val}

# Response:
# {status: ok|error, data:{...}}