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
from flask_login import login_required
from bundesliga_tippspiel import app
from bundesliga_tippspiel.utils.routes import api, api_login_required
from bundesliga_tippspiel.actions.DeleteUserAction import DeleteUserAction
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction
from bundesliga_tippspiel.actions.ApiKeyGenAction import ApiKeyGenAction
from bundesliga_tippspiel.actions.ApiKeyDeleteAction import ApiKeyDeleteAction
from bundesliga_tippspiel.actions.ChangePasswordAction import \
    ChangePasswordAction
from bundesliga_tippspiel.actions.ForgotPasswordAction import \
    ForgotPasswordAction


@app.route("/api/v2/register", methods=["POST"])
@api
def api_register():
    """
    Allows registering a user using the API
    :return: The JSON response
    """
    action = RegisterAction.from_dict(request.get_json())
    return action.execute()


@app.route("/api/v2/forgot", methods=["POST"])
@api
def api_forgot():
    """
    Allows users to reset their password using the API
    :return: The JSON response
    """
    action = ForgotPasswordAction.from_dict(request.get_json())
    return action.execute()


@app.route("/api/v2/api_key", methods=["POST", "DELETE"])
@api
def api_api_key():
    """
    Allows users to request a new API key or revoke an existing API key
    :return: The JSON response
    """
    if request.method == "POST":
        action = ApiKeyGenAction.from_dict(request.get_json())
    else:  # request.method == "DELETE"
        action = ApiKeyDeleteAction.from_dict(request.get_json())
    return action.execute()


@app.route("/api/v2/authorize", methods=["GET"])
@api_login_required
@login_required
@api
def api_authorize():
    """
    Allows a user to check if an API key is authorized or not
    :return: None
    """
    return {}  # Checks done by @login_required


@app.route("/api/v2/delete_user", methods=["POST"])
@api_login_required
@login_required
@api
def api_delete_user():
    """
    Allows a user to delete their account
    :return: The JSON response
    """
    action = DeleteUserAction.from_dict(request.get_json())
    return action.execute()


@app.route("/api/v2/change_password", methods=["POST"])
@api_login_required
@login_required
@api
def api_change_password():
    """
    Allows a user to change their password
    :return: The JSON response
    """
    action = ChangePasswordAction.from_dict(request.get_json())
    return action.execute()
