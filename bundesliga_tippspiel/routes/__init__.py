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
from bundesliga_tippspiel.routes.information import define_blueprint \
    as __information
from bundesliga_tippspiel.routes.email_reminder import define_blueprint \
    as __email_reminder
from bundesliga_tippspiel.routes.api.putters import define_blueprint \
    as __putters
from bundesliga_tippspiel.routes.api.getters import define_blueprint \
    as __getters

from flask.blueprints import Blueprint
from typing import List, Tuple, Callable

blueprint_generators: List[Tuple[Callable[[str], Blueprint], str]] = [
    (__email_reminder, "email_reminder"),
    (__information, "information"),
    (__putters, "putters"),
    (__getters, "getters"),
    (__betting, "betting")
]
"""
Defines the functions used to create the various blueprints
as well as their names
"""
