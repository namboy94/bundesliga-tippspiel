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

from flask import jsonify
from bundesliga_tippspiel import app

# API buildup:
# Send JSON TO URL using GET/POST/PUT etc
# Format:
# {"email": <email>, "key": <api key>, "data": {...}}
# Receive JSON response with "status": {success, error}
# If error: reason
# If success: data


@app.route("/api/v2/register", methods=["POST"])
def api_register():
    """
    Provides an API route for registering a new user
    :return: The JSON response
    """
    # json_data = request.get_json()
    return jsonify({"Test": 1})
