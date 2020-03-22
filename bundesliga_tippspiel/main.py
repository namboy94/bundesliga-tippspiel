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
from typing import List
from flask.blueprints import Blueprint
from puffotter.flask.base import db
from puffotter.flask.initialize import init_flask
from puffotter.flask.wsgi import start_server
from bundesliga_tippspiel.db.match_data.Player import Player
from bundesliga_tippspiel.db.match_data.Goal import Goal
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.user_generated.EmailReminder import EmailReminder
from bundesliga_tippspiel.routes.betting import betting_blueprint
from bundesliga_tippspiel.routes.information import information_blueprint
from bundesliga_tippspiel.routes.static import static_blueprint
from bundesliga_tippspiel.routes.authentification import \
    authentification_blueprint
from bundesliga_tippspiel.routes.user_management import \
    user_management_blueprint
from bundesliga_tippspiel.routes.api.putters import putters_blueprint
from bundesliga_tippspiel.routes.api.getters import getters_blueprint
from bundesliga_tippspiel.routes.api.user_management import \
    user_management_api_blueprint
from bundesliga_tippspiel.bg_tasks import bg_tasks
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel import sentry_dsn


blueprints: List[Blueprint] = [
    betting_blueprint,
    information_blueprint,
    static_blueprint,
    authentification_blueprint,
    user_management_blueprint,
    putters_blueprint,
    getters_blueprint,
    user_management_api_blueprint
]
"""
The route blueprints of the application
"""

models: List[db.Model] = [
    Player,
    Goal,
    Match,
    Team,
    Bet,
    EmailReminder
]
"""
The database models of the application
"""

root_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)))
"""
The root path of the application
"""


def main():

    init_flask(
        "bundesliga_tippspiel",
        sentry_dsn,
        root_path,
        Config,
        models,
        blueprints
    )
    start_server(Config, bg_tasks)
