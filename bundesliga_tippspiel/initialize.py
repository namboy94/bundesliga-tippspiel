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

import bundesliga_tippspiel.globals as glob
from flask_sqlalchemy import SQLAlchemy


def initialize_db():

    if glob.app.config["ENV"] == "production":
        db_uri = "sqlite:////tmp/test.db"
    elif glob.app.config["TESTING"]:
        db_uri = "sqlite://test.db"
    else:
        db_uri = "sqlite:////tmp/test.db"

    glob.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    glob.db = SQLAlchemy(glob.app)


# noinspection PyUnresolvedReferences
def initialize_db_models():
    from bundesliga_tippspiel.models.match_data.Team import Team
    from bundesliga_tippspiel.models.match_data.Goal import Goal
    from bundesliga_tippspiel.models.match_data.Match import Match
    from bundesliga_tippspiel.models.match_data.Player import Player
    glob.db.create_all()
