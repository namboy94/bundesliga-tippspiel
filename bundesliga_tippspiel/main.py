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

from puffotter.env import load_env_file
from jerrycan.initialize import init_flask
from jerrycan.wsgi import start_server
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel import sentry_dsn, root_path
from bundesliga_tippspiel.background import bg_tasks
from bundesliga_tippspiel.db import models
from bundesliga_tippspiel.routes import blueprint_generators
from bundesliga_tippspiel.jinja_extras import jinja_extras


def main():  # pragma: no cover
    """
    Initializes and starts the flask application
    :return: None
    """
    load_env_file()
    init_flask(
        "bundesliga_tippspiel",
        sentry_dsn,
        root_path,
        Config,
        models,
        blueprint_generators,
        jinja_extras()
    )
    start_server(Config, bg_tasks)
