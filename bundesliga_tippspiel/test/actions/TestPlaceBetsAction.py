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

from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.PlaceBetsAction import PlaceBetsAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.actions.ActionTestFramework import\
    _ActionTestFramework


class TestPlaceBetsAction(_ActionTestFramework):
    """
    Test class that tests the place bets action
    """

    def setUp(self):
        """
        Sets up a user in the database
        :return: None
        """
        super().setUp()
        self.user = self.generate_sample_user(True)["user"]
        self.team_one, self.team_two, _, _, _ = \
            self.generate_sample_match_data()
        self.match_one = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=True
        )
        self.match_two = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=False, finished=False
        )
        self.match_three = Match(
            home_team=self.team_one, away_team=self.team_two,
            matchday=1, kickoff="2019-01-01:01:02:03",
            started=True, finished=False
        )
        self.db.session.add(self.match_one)
        self.db.session.add(self.match_two)
        self.db.session.add(self.match_three)
        self.db.session.commit()

    def generate_action(self) -> PlaceBetsAction:
        """
        Generates a new, valid Action object
        :return: The generated object
        """
        return PlaceBetsAction(
            {
                self.match_one.id: (2, 1),
                self.match_two.id: (0, 3)
            }
        )

    def test_placing_bets(self):
        """
        Tests placing bets.
        :return:
        """
        with self.context:
            self.login_user(self.user)

            resp = self.action.execute()
            self.assertEqual(resp["new"], 2)
            self.assertEqual(resp["updated"], 0)
            self.assertEqual(resp["invalid"], 0)

            bets = Bet.query.filter_by(user_id=self.user.id).all()
            self.assertEqual(len(bets), 2)

            self.assert_bet(self.match_one.id, 2, 1)
            self.assert_bet(self.match_two.id, 0, 3)

    def test_updating_bets(self):
        """
        Tests placing bets again
        :return: None
        """
        with self.context:
            self.login_user(self.user)

            self.action.execute()
            self.action.bets = {
                self.match_one.id: (5, 0),
                self.match_two.id: (0, 0)
            }
            resp = self.action.execute()
            self.assertEqual(resp["new"], 0)
            self.assertEqual(resp["updated"], 2)
            self.assertEqual(resp["invalid"], 0)

            bets = Bet.query.filter_by(user_id=self.user.id).all()
            self.assertEqual(len(bets), 2)

            self.assert_bet(self.match_one.id, 5, 0)
            self.assert_bet(self.match_two.id, 0, 0)

    def test_invalid_bets(self):
        """
        Tests using invalid data to place bets.
        :return: None
        """
        with self.context:
            self.login_user(self.user)

            self.action.bets = {
                self.match_one.id: ("Five", 0),
                "self.match_two.id": (0, 0),
                self.match_three.id: (0, 0),
                100: (3, 4),
            }
            resp = self.action.execute()
            self.assertEqual(resp["new"], 0)
            self.assertEqual(resp["updated"], 0)
            self.assertEqual(resp["invalid"], 4)

            bets = Bet.query.filter_by(user_id=self.user.id).all()
            self.assertEqual(len(bets), 0)

    def test_bets_out_of_bounds(self):
        """
        Tests using bets that are out of bounds
        :return: None
        """
        with self.context:
            self.login_user(self.user)

            self.action.bets = {
                self.match_one.id: (-1, 0),
                self.match_three.id: (100, 0)
            }
            resp = self.action.execute()
            self.assertEqual(resp["new"], 0)
            self.assertEqual(resp["updated"], 0)
            self.assertEqual(resp["invalid"], 2)

            bets = Bet.query.filter_by(user_id=self.user.id).all()
            self.assertEqual(len(bets), 0)

    def test_mixing_valid_and_invalid_bets(self):
        """
        Tests placing both valid and invalid bets
        :return: None
        """
        with self.context:
            self.login_user(self.user)

            self.action.bets = {
                self.match_one.id: (5, 0),
                self.match_three.id: (0, 0)
            }
            resp = self.action.execute()
            self.assertEqual(resp["new"], 1)
            self.assertEqual(resp["updated"], 0)
            self.assertEqual(resp["invalid"], 1)

            bets = Bet.query.filter_by(user_id=self.user.id).all()
            self.assertEqual(len(bets), 1)

    def test_parsing_form_data(self):
        """
        Tests if parsing the form data works correctly
        :return: None
        """
        form_data = {
            "{}-home".format(self.match_one.id): "1",
            "{}-away".format(self.match_one.id): "2",
            "{}-home".format(self.match_two.id): "1",
            str(self.match_three.id): "1",
            "Irrelevant": "Stuff",
            "{}-home".format(self.match_three.id): "A",
            "{}-away".format(self.match_three.id): "B",
            "{}-blabla".format(self.match_three.id): "1"
        }
        action = PlaceBetsAction.from_dict(form_data)
        self.assertEqual(action.bets, {
            self.match_one.id: (1, 2),
            3: (1, None),
            4: (None, None)
        })
        action.validate_data()
        self.assertEqual(action.bets, {
            self.match_one.id: (1, 2)
        })
        self.assertEqual(action.error_count, 2)

    def assert_bet(self, match_id: int, home: int, away: int):
        """
        Tests that a stored bet has the specified parameters
        :param match_id: The match ID of the bet to test
        :param home: The home score to check for
        :param away: The away score to check for
        :return: None
        """
        bet = Bet.query.filter_by(
            user_id=self.user.id, match_id=match_id
        ).first()
        self.assertEqual(bet.home_score, home)
        self.assertEqual(bet.away_score, away)
