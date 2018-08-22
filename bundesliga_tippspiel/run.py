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

import os
import pkg_resources
from bundesliga_tippspiel import app
from bundesliga_tippspiel.routes import load_routes
from bundesliga_tippspiel.utils.db import initialize_db
from bundesliga_tippspiel.config import db_user, db_key, db_name

if not app.testing:  # pragma: no cover

    app.secret_key = os.environ["FLASK_SECRET"]

    if app.config["ENV"] == "production":
        uri = "mysql://{}:{}@localhost:3306/{}".format(
            db_user, db_key, db_name
        )
    else:
        uri = "sqlite:////tmp/bundesliga_tippspiel.db"

    initialize_db(uri)
    load_routes()


@app.context_processor
def inject_template_variables():
    """
    Injects the project's version string so that it will be available
    in templates
    :return: The dictionary to inject
    """
    version = pkg_resources.get_distribution("bundesliga-tippspiel").version
    return {
        "version": version,
        "env": app.env
    }
