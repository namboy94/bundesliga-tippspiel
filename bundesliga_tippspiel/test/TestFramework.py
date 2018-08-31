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
import bundesliga_tippspiel
from functools import wraps
from unittest import TestCase
from typing import Tuple, Callable, Dict
from flask_login import login_user
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.models.match_data.Player import Player
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.match_data.Goal import Goal
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.auth.ApiKey import ApiKey
from bundesliga_tippspiel.utils.crypto import generate_random
from bundesliga_tippspiel.utils.match_data_getter import update_db_data
from bundesliga_tippspiel.utils.initialize import initialize_app, \
    initialize_login_manager, initialize_db


class _TestFramework(TestCase):
    """
    Class that models a testing framework for the flask application
    """

    # Constants
    API_KEY = "apikey"
    API_KEY_HASH = \
        b"$2b$12$hZgUP0mzn6pZsQ45FYkiJuZFIRDCo.MbDb7e2fGHAJJq/jqn9yf9e"

    def setUp(self):
        """
        Sets up the SQLite database
        :return: None
        """
        bundesliga_tippspiel.app.config["TESTING"] = True
        self.db_path = os.path.join(os.path.abspath("."), "test.db")

        self.cleanup()

        self.app = bundesliga_tippspiel.app
        self.db = bundesliga_tippspiel.db

        self.app.secret_key = generate_random(20)

        initialize_app()
        initialize_db("sqlite:///{}".format(self.db_path))
        self.app.app_context().push()
        initialize_login_manager()

        self.client = self.app.test_client()
        self.context = self.app.test_request_context()

    def tearDown(self):
        """
        Deletes the test database if it exists
        :return: None
        """
        self.cleanup()

    def cleanup(self):
        """
        Deletes the SQLite database file
        :return: None
        """
        try:
            os.remove(self.db_path)
        except FileNotFoundError:
            pass

    def generate_sample_match_data(self) \
            -> Tuple[Team, Team, Player, Match, Goal]:
        """
        Generates some sample match data
        :return: A tuple consisting of two teams, a player, a match and a goal
        """

        team_one = Team(
            name="A", short_name="B", abbreviation="C",
            icon_svg="D1", icon_png="D2"
        )
        team_two = Team(
            name="E", short_name="F", abbreviation="G",
            icon_svg="H1", icon_png="H2"
        )
        player = Player(name="I", team=team_one)
        match = Match(
            matchday=1, kickoff="2017-01-01:01-02-03",
            finished=True, started=True,
            home_team=team_one, away_team=team_two,
            home_current_score=1, away_current_score=0,
            home_ht_score=0, away_ht_score=0,
            home_ft_score=1, away_ft_score=0
        )
        goal = Goal(
            match=match, player=player, minute=67, minute_et=None,
            home_score=1, away_score=0, own_goal=False, penalty=False
        )

        self.db.session.add(team_one)
        self.db.session.add(team_two)
        self.db.session.add(player)
        self.db.session.add(match)
        self.db.session.add(goal)
        self.db.session.commit()

        return team_one, team_two, player, match, goal

    def generate_sample_bet(self, user: User, match: Match) -> Bet:
        """
        Generates a sample bet betting 2:1
        :param user: The user for which to generate the bet
        :param match: The match for which to generate the bet
        :return: The bet
        """
        bet = Bet(user=user, match=match, home_score=2, away_score=1)
        self.db.session.add(bet)
        self.db.session.commit()
        return bet

    def generate_sample_user(self, confirmed: bool) -> Dict[str, User or str]:
        """
        Generates a sample user
        Instead of hashing the passwords each time, we simply use hard-coded
        values.
        :return: A dictionary containing the sample user as well as their
                 password. The password doubles as a confirmation key
        """
        if confirmed:
            password = "samplepass1"
            hashed = \
                b"$2b$12$BiB2kya1Ly3wuY/Pr4JGD.JSmmd1ocTWoAH9OPAbSqyT.CQ5./pUi"
            user = User(username="TestA", email="a@hk-tippspiel.com",
                        password_hash=hashed.decode("utf-8"), confirmed=True,
                        confirmation_hash=hashed)
        else:
            password = "samplepass2"
            hashed = \
                b"$2b$12$ygmgJH2JFaMqGwBO5F3w.u7ROKuwnC0V/Erneb5Udklgqjija8kfS"
            user = User(username="TestB", email="b@hk-tippspiel.com",
                        password_hash=hashed.decode("utf-8"), confirmed=False,
                        confirmation_hash=hashed)

        self.db.session.add(user)
        self.db.session.commit()

        return {"user": user, "pass": password}

    def generate_sample_users(self) \
            -> Tuple[Dict[str, User or str], Dict[str, User or str]]:
        """
        Generates two users, one confirmed, one unconfirmed
        :return: The two users as tuple
        """
        return \
            self.generate_sample_user(True),\
            self.generate_sample_user(False)

    def generate_sample_api_key(self, user: User):
        """
        Generates an API key for a user
        :param user: The user for which to generate the API key
        :return: The Api key object
        """
        obj = ApiKey(user=user, key_hash=self.API_KEY_HASH.decode("utf-8"))
        self.db.session.add(obj)
        self.db.session.commit()
        return obj

    @staticmethod
    def online_required(func: Callable):
        """
        Decorator that skips tests that require online connectivity if
        the NO_ONLINE environment variable is set to 1
        :param func: The function to wrap
        :return: The wrapper function
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if "NO_ONLINE" in os.environ and os.environ["NO_ONLINE"] == "1":
                pass
            else:
                func(*args, **kwargs)

        return wrapper

    def login_user(self, user: User):
        """
        Logs in a user in the local context
        :param user: The user to log in
        :return: None
        """
        with self.context:
            login_user(user)

    @staticmethod
    def load_real_match_data():
        """
        Loads real match data from openligadb.com into the database
        :return: None
        """
        update_db_data()
