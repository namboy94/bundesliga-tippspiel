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
import logging
from flask.logging import default_handler
from bundesliga_tippspiel import app
from bundesliga_tippspiel.config import db_user, db_key, db_name, logging_path
from bundesliga_tippspiel.utils.initialize import initialize_db, \
    initialize_app, initialize_login_manager


if not app.testing:  # pragma: no cover

    app.secret_key = os.environ["FLASK_SECRET"]

    if app.config["ENV"] == "production":
        uri = "mysql://{}:{}@localhost:3306/{}".format(
            db_user, db_key, db_name
        )
    else:
        uri = "sqlite:////tmp/bundesliga_tippspiel.db"

    initialize_app()
    initialize_db(uri)
    initialize_login_manager()

    app.logger.removeHandler(default_handler)

    logging.basicConfig(
        filename=logging_path,
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    app.logger.error("STARTING FLASK")
    app.logger.warning("STARTING FLASK")
    app.logger.info("STARTING FLASK")
    app.logger.debug("STARTING FLASK")
