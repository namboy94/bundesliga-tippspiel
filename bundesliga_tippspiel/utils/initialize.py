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

import base64
import pkg_resources
from binascii import Error
from typing import Optional
from bundesliga_tippspiel.routes import load_routes
from bundesliga_tippspiel import app, db, login_manager
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey


def initialize_app():
    """
    Initializes the App
    :return: None
    """
    @app.context_processor
    def inject_template_variables():
        """
        Injects the project's version string so that it will be available
        in templates
        :return: The dictionary to inject
        """
        version = \
            pkg_resources.get_distribution("bundesliga-tippspiel").version
        return {
            "version": version,
            "env": app.env
        }

    load_routes()


# noinspection PyUnresolvedReferences
def initialize_db(db_uri: str):
    """
    Initializes the SQLAlchemy database
    :param db_uri: The URI of the database to initialize
    :return: None
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from bundesliga_tippspiel.models.match_data.Team import Team
    from bundesliga_tippspiel.models.match_data.Goal import Goal
    from bundesliga_tippspiel.models.match_data.Match import Match
    from bundesliga_tippspiel.models.match_data.Player import Player
    from bundesliga_tippspiel.models.auth.User import User
    from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
    from bundesliga_tippspiel.models.user_generated.Bet import Bet

    with app.app_context():
        db.create_all()


def initialize_login_manager():
    """
    Initializes the login manager
    :return: None
    """
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
            api_key = base64.b64decode(api_key.encode("utf-8")).decode("utf-8")
        except (TypeError, Error):  # pragma: no cover
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
