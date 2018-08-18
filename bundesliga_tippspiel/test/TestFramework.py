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
import bundesliga_tippspiel.globals as glob
from typing import Tuple, Callable
from unittest import TestCase

from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.models.match_data.Player import Player
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.match_data.Goal import Goal


class TestFramework(TestCase):
    """
    Class that models a testing framework for the flask application
    """

    def setUp(self):
        """
        Sets up the SQLite database
        :return: None
        """
        glob.app.config["TESTING"] = True
        self.db_path = os.path.join(os.path.abspath("."), "test.db")

        self.cleanup()

        self.app = glob.app
        self.db = glob.db
        glob.initialize_db("sqlite:///{}".format(self.db_path))
        self.app.app_context().push()

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


def online_required(test_func: Callable):
    """
    Decorator that skips tests that require online connectivity if
    the NO_ONLINE environment variable is set to 1
    :param test_func: The function to wrap
    :return: The wrapper function
    """

    def test_wrapper(*args, **kwargs):
        if "NO_ONLINE" in os.environ and os.environ["NO_ONLINE"] == "1":
            pass
        else:
            test_func(*args, **kwargs)

    return test_wrapper
