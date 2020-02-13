"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of fat-ffipd.

fat-ffipd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fat-ffipd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fat-ffipd.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import base64
import logging
import random
import string
from binascii import Error
from typing import Optional
from flask.logging import default_handler
from flask import redirect, url_for, flash, render_template
from werkzeug.exceptions import HTTPException
from bundesliga_tippspiel.config import Config
from bundesliga_tippspiel.db.auth.User import User
from bundesliga_tippspiel.db.auth.ApiKey import ApiKey
from bundesliga_tippspiel.db.models import create_tables
from bundesliga_tippspiel.enums import AlertSeverity
from bundesliga_tippspiel.flask import app, db, login_manager
from bundesliga_tippspiel.routes.blueprints import register_blueprints


def init():
    """
    Initializes the Flask application
    :return:
    """

    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    login_manager.session_protection = "strong"

    if "FLASK_TESTING" in os.environ:
        app.testing = os.environ["FLASK_TESTING"] == "1"

    @app.context_processor
    def inject_template_variables():
        """
        Injects the project's version string so that it will be available
        in templates
        :return: The dictionary to inject
        """
        return {
            "version": Config().version,
            "env": app.env
        }

    try:
        app.secret_key = os.environ["FLASK_SECRET"]
    except KeyError:
        app.secret_key = "".join(random.choice(string.ascii_letters)
                                 for _ in range(0, 32))
        app.logger.warning("No secret key provided")

    app.config["SQLALCHEMY_DATABASE_URI"] = Config().db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    register_blueprints(app)
    create_tables(app, db)

    # Set up login manager
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """
        Loads a user from an ID
        :param user_id: The ID
        :return: The User
        """
        return User.query.get(int(user_id))

    @login_manager.request_loader
    def load_user_from_request(request) -> Optional[User]:
        """
        Loads a user pased on a provided API key
        :param request: The request containing the API key in the headers
        :return: The user or None if no valid API key was provided
        """
        if "Authorization" not in request.headers:
            return None

        api_key = request.headers["Authorization"].replace("Basic ", "", 1)

        try:
            api_key = base64.b64decode(
                api_key.encode("utf-8")
            ).decode("utf-8")
        except (TypeError, Error):
            pass

        db_api_key = ApiKey.query.get(api_key.split(":", 1)[0])

        # Check for validity of API key
        if db_api_key is None or not db_api_key.verify_key(api_key):
            return None

        elif db_api_key.has_expired():
            db.session.delete(db_api_key)
            db.session.commit()
            return None

        return User.query.get(db_api_key.user_id)

    @app.errorhandler(HTTPException)
    def error_handling(error: HTTPException):
        """
        Custom redirect for 401 errors
        :param error: The error that caused the error handler to be called
        :return: A redirect to the login page
        """
        if error.code == 401:
            flash(
                "Du bist nicht angemeldet. Bitte melde dich an.",
                AlertSeverity.DANGER.value
            )
            return redirect(url_for("authentication.login"))
        else:
            return render_template("static/error_page.html", error=error)

    app.logger.removeHandler(default_handler)

    logging.basicConfig(
        filename=Config().logging_path,
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    app.logger.error("STARTING FLASK")
    app.logger.warning("STARTING FLASK")
    app.logger.info("STARTING FLASK")
    app.logger.debug("STARTING FLASK")
