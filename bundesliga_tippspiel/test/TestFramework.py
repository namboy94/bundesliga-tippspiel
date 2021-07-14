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

# noinspection PyProtectedMember
from jerrycan.test.TestFramework import _TestFramework as Framework
from typing import Tuple
from jerrycan.db.User import User
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.match_data.Player import Player
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Goal import Goal
from bundesliga_tippspiel.background.openligadb import update_match_data
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel import root_path
from bundesliga_tippspiel.routes import blueprint_generators
from bundesliga_tippspiel.main import models
from bundesliga_tippspiel.jinja_extras import jinja_extras


class _TestFramework(Framework):
    """
    Class that models a testing framework for the flask application
    """

    module_name = "bundesliga_tippspiel"
    root_path = root_path
    models = models
    config = Config
    blueprint_generators = blueprint_generators
    extra_jinja_vars = jinja_extras()

    def setUp(self):
        """
        Sets up the flask application and a temporary database to test with
        :return: None
        """
        super().setUp()
        self.config.OPENLIGADB_LEAGUE = "bl1"
        self.config.OPENLIGADB_SEASON = "2018"

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
        player = Player(
            name="I",
            team_abbreviation=team_one.abbreviation
        )
        match = Match(
            matchday=1, kickoff="2017-01-01:01-02-03",
            finished=True, started=True,
            home_team_abbreviation=team_one.abbreviation,
            away_team_abbreviation=team_two.abbreviation,
            home_current_score=1, away_current_score=0,
            home_ht_score=0, away_ht_score=0,
            home_ft_score=1, away_ft_score=0,
            season=self.config.season(),
            league=self.config.OPENLIGADB_LEAGUE
        )
        goal = Goal(
            home_team_abbreviation=match.home_team_abbreviation,
            away_team_abbreviation=match.away_team_abbreviation,
            season=match.season,
            league=match.league,
            matchday=match.matchday,
            player_name=player.name,
            player_team_abbreviation=player.team_abbreviation,
            minute=67, minute_et=None,
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
        bet = Bet(
            user=user,
            home_team_abbreviation=match.home_team_abbreviation,
            away_team_abbreviation=match.away_team_abbreviation,
            season=match.season,
            league=match.league,
            matchday=match.matchday,
            home_score=2,
            away_score=1,
            points=0
        )
        self.db.session.add(bet)
        self.db.session.commit()
        return bet

    @staticmethod
    def load_real_match_data():
        """
        Loads real match data from openligadb.com into the database
        :return: None
        """
        update_match_data()
