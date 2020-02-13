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

from flask import request, url_for, redirect, render_template, Blueprint
from flask_login import login_required, logout_user, current_user
from bundesliga_tippspiel.flask import app
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.actions.LoginAction import LoginAction

authentification_blueprint = Blueprint("authentication", __name__)


@authentification_blueprint.route("/login", methods=["GET", "POST"])
@action_route
def login():
    """
    Page that allows the user to log in
    :return: The generated HTML
    """

    if request.method == "GET":
        return render_template("profile/login.html")
    else:  # request.method == "POST"
        action = LoginAction.from_site_request()
        return action.execute_with_redirects(
            "static.index",
            "Du hast dich erfolgreich angemeldet.",
            "authentication.login"
        )


@authentification_blueprint.route("/logout")
@login_required
@action_route
def logout():
    """
    Logs out the user
    :return:
    """
    app.logger.info("User {} logged out.".format(current_user.username))
    logout_user()
    return redirect(url_for("static.index"))
