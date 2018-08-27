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
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel import app
from flask import render_template, request
from bundesliga_tippspiel.actions.ConfirmAction import ConfirmAction
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Page that allows a new user to register
    :return: The generated HTML
    """

    if request.method == "GET":
        return render_template("register.html")
    else:  # request.method == "POST"
        action = RegisterAction.from_site_request()
        success_msg = "Siehe in deiner Email-Inbox nach, " \
                      "um die Registrierung abzuschließen."
        return action.execute_with_redirects(
            "index",
            ActionException(success_msg, success_msg)
        )


@app.route("/confirm", methods=["GET"])
def confirm():
    """
    Confirms a user
    :return: The appropriate redirect
    """
    action = ConfirmAction.from_site_request()
    return action.execute_with_redirects(
        "login",
        "Benutzer wurde erfolgreich registriert. "
        "Du kannst dich jetzt anmelden.",
        "index"
    )


@app.route("/forgot")
def forgot():
    """
    Allows a user to reset their password
    :return: None
    """
    return render_template("index.html")
