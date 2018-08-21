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

# noinspection PyUnresolvedReferences
import bundesliga_tippspiel.api
from flask import render_template, request, flash, redirect, url_for
from bundesliga_tippspiel.globals import app, initialize_db
from bundesliga_tippspiel.config import db_key, db_name, db_user
from bundesliga_tippspiel.exceptions import ActionException
from bundesliga_tippspiel.actions.RegisterAction import RegisterAction


if app.config["ENV"] == "production" \
        and not app.config["TESTING"]:  # pragma: no cover
    uri = "mysql://{}:{}@localhost:3306/{}".format(db_user, db_key, db_name)
else:
    uri = "sqlite:////tmp/bundesliga_tippspiel.db"

if not app.config["TESTING"]:  # pragma: no cover
    initialize_db(uri)


# Pages

@app.route("/")
def index():
    """
    The index/home page
    :return: The generated HTML
    """
    return render_template("index.html")


@app.route("/about")
def about():
    """
    The about page/"Impressum" for the website
    :return: The generated HTML
    """
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    """
    Page containing a privacy disclaimer
    :return: The generated HTML
    """
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Page that allows a new user to register
    :return: The generated HTML
    """

    if request.method == "GET":
        return render_template("register.html")
    else:
        action = RegisterAction.from_site_request()

        try:
            action.execute()
            flash("Siehe in deiner Email-Inbox nach, "
                  "um die Registrierung abzuschließen.", "info")
            return redirect(url_for("index"))

        except ActionException as e:
            e.flash()
            return redirect(url_for("register"))


@app.route("/login")
def login():
    return "Login"


@app.route("/logout")
def logout():
    return "Logout"


@app.route("/bets")
def bets():
    return "Bets"


@app.route("/leaderboard")
def leaderboard():
    return "Leaderboard"


@app.route("/profile")
def profile():
    return "Profile"
