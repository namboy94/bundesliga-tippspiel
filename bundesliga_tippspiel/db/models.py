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
from flask_sqlalchemy import SQLAlchemy


# noinspection PyUnresolvedReferences
def create_tables(app: Flask, db: SQLAlchemy):
    """
    Creates all tables in the database if they don't exist yet
    :param app: The flask application
    :param db: The database
    :return: None
    """
    from bundesliga_tippspiel.db.auth.User import User
    from bundesliga_tippspiel.db.auth.ApiKey import ApiKey
    from bundesliga_tippspiel.db.match_data.Player import Player
    from bundesliga_tippspiel.db.match_data.Goal import Goal
    from bundesliga_tippspiel.db.match_data.Match import Match
    from bundesliga_tippspiel.db.match_data.Team import Team
    from bundesliga_tippspiel.db.user_generated.Bet import Bet
    from bundesliga_tippspiel.db.user_generated.EmailReminder import \
        EmailReminder
    with app.app_context():
        db.create_all()
