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

from bundesliga_tippspiel.routes.betting import define_blueprint as __betting
from bundesliga_tippspiel.routes.info import define_blueprint as __info
from bundesliga_tippspiel.routes.settings import define_blueprint as __settings
from bundesliga_tippspiel.routes.stats import define_blueprint as __stats
from bundesliga_tippspiel.routes.tables import define_blueprint as __tables
from bundesliga_tippspiel.routes.chat import define_blueprint as __chat
from bundesliga_tippspiel.routes.api.betting import \
    define_blueprint as __api_betting
from bundesliga_tippspiel.routes.api.info import define_blueprint as __api_info

from flask.blueprints import Blueprint
from typing import List, Tuple, Callable

blueprint_generators: List[Tuple[Callable[[str], Blueprint], str]] = [
    (__info, "info"),
    (__betting, "betting"),
    (__settings, "settings"),
    (__chat, "chat"),
    (__tables, "tables"),
    (__stats, "stats"),
    (__api_betting, "api_betting"),
    (__api_info, "api_info")
]
"""
Defines the functions used to create the various blueprints
as well as their names
"""
