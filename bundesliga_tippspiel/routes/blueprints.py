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

from flask import Flask
from bundesliga_tippspiel.routes.betting import betting_blueprint
from bundesliga_tippspiel.routes.information import information_blueprint
from bundesliga_tippspiel.routes.static import static_blueprint
from bundesliga_tippspiel.routes.authentification import \
    authentification_blueprint
from bundesliga_tippspiel.routes.user_management import \
    user_management_blueprint
from bundesliga_tippspiel.routes.api.putters import putters_blueprint
from bundesliga_tippspiel.routes.api.getters import getters_blueprint
from bundesliga_tippspiel.routes.api.update import update_blueprint
from bundesliga_tippspiel.routes.api.user_management import \
    user_management_api_blueprint


def register_blueprints(app: Flask):
    """
    Registers all route blueprints in the flask app
    :param app: The flask application
    :return: None
    """
    for blueprint in [
        betting_blueprint,
        information_blueprint,
        static_blueprint,
        authentification_blueprint,
        user_management_blueprint,
        putters_blueprint,
        getters_blueprint,
        update_blueprint,
        user_management_api_blueprint
    ]:
        app.register_blueprint(blueprint)
