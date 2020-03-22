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
from typing import Type
from puffotter.flask.Config import Config as BaseConfig


class Config(BaseConfig):
    """
    Configuration for the flask application
    """
    OPENLIGADB_SEASON: str
    """
    The openligadb season to use
    """

    OPENLIGADB_LEAGUE: str
    """
    The openligadb league to use
    """

    @classmethod
    def _load_extras(cls, parent: Type[BaseConfig]):
        """
        Loads non-standard configuration variables
        :param parent: The base configuration
        :return: None
        """
        Config.OPENLIGADB_SEASON = os.environ.get("OPENLIGADB_SEASON", "2019")
        Config.OPENLIGADB_LEAGUE = os.environ.get("OPENLIGADB_LEAGUE", "bl1")
        parent.STRINGS.update({
            "401_message": "Du bist nicht angemeldet. Bitte melde dich an."
        })
