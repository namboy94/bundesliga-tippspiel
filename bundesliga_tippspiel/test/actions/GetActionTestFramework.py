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

from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.match_data.Goal import Goal
from bundesliga_tippspiel.models.match_data.Player import Player
from bundesliga_tippspiel.models.match_data.Team import Team
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import \
    _ActionTestFramework
from bundesliga_tippspiel.types.exceptions import ActionException


class _GetActionTestFramework(_ActionTestFramework):
    """
    Framework for testing 'Get' Action classes
    """

    def setUp(self):
        """
        Populates the database with sample data for testing
        :return: None
        """
        super().setUp()
        self.team_one, self.team_two, self.player_one, \
            self.match_one, self.goal_one = self.generate_sample_match_data()
        self.match_two = Match(
            home_team=self.team_two,
            away_team=self.team_one,
            matchday=18,
            kickoff="2019-01-01:01:02:03",
            started=False,
            finished=False
        )
        self.user_one, self.user_two = self.generate_sample_users()
        self.user_one = self.user_one["user"]
        self.user_two = self.user_two["user"]
        self.bet_one = self.generate_sample_bet(self.user_one, self.match_one)
        self.bet_two = self.generate_sample_bet(self.user_two, self.match_one)
        self.bet_three = \
            self.generate_sample_bet(self.user_one, self.match_two)
        self.team_three = Team(name="1", short_name="2", abbreviation="3",
                               icon_png="4", icon_svg="5")
        self.player_two = Player(team=self.team_three, name="TestPlayer")
        self.goal_two = Goal(match=self.match_two, player=self.player_two,
                             minute=1, home_score=1, away_score=1)

        self.db.session.add(self.match_two)
        self.db.session.add(self.goal_two)
        self.db.session.add(self.player_two)
        self.db.session.add(self.goal_two)
        self.db.session.add(self.team_three)
        self.db.session.commit()

    @property
    def action_cls(self) -> type(Action):
        """
        :return: The tested Action class
        """
        raise NotImplementedError()

    def generate_action(self) -> Action:
        """
        Generates a new, valid Action object
        :return: The generated object
        """
        return self.action_cls()

    def test_using_filter_and_id(self):
        """
        Tests that using an ID and an explicit filter does not work
        :return: None
        """
        raise NotImplementedError()

    def test_fetching(self):
        """
        Tests fetching using different methods
        :return: None
        """
        raise NotImplementedError()

    def test_finding_invalid_id(self):
        """
        Tests finding an invalid ID
        :return: None
        """
        self.action.id = 0
        self.failed_execute("ID does not exist", 404)

    def test_using_invalid_matchday(self):
        """
        Tests using invalid matchdays
        :return: None
        """
        if hasattr(self.action, "matchday"):
            for matchday in [0, 35]:
                self.action.matchday = matchday
                self.failed_execute("Matchday out of bounds")

    def test_from_dict(self):
        """
        Tests generating an action from a dictionary
        :return: None
        """
        fetch_all = self.action_cls.from_dict({})
        self.assertEqual(fetch_all.id, None)

        fetch_id = self.action_cls.from_dict({"id": 1})
        self.assertEqual(fetch_id.id, 1)

        try:
            wrong_type = self.action_cls.from_dict({"id": "one"})
            wrong_type.execute()
            self.fail()
        except ActionException as e:
            self.assertEqual(e.reason, "invalid parameters")
