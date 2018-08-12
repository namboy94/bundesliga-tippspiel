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

from bundesliga_tippspiel.globals import app, initialize_db
from flask import render_template

if app.config["ENV"] == "production":
    uri = "sqlite:////tmp/test.db"
else:
    uri = "sqlite:////tmp/bundesliga_tippspiel.db"
initialize_db(uri)


@app.route("/")
def index():
    """
    The index/home page
    :return: The generated HTML
    """
    return render_template("index.html")


@app.route("/env")
def env():
    return app.config["ENV"]