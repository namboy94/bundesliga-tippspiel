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

from typing import Tuple, List, Dict, Any
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.utils.json import jsonify_models
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.ApiRouteTestFramework import \
    _ApiRouteTestFramework


class _GetterApiRouteTestFramework(_ApiRouteTestFramework):
    """
    Test framework for GETter API endpoints
    """

    def setUp(self):
        """
        Sets up some test data
        :return: None
        """
        super().setUp()
        self.team_one, self.team_two, self.player, self.match, self.goal = \
            self.generate_sample_match_data()
        self.bet = self.generate_sample_bet(self.user, self.match)

    @property
    def keyword(self) -> str:
        """
        :return: The route keyword. Example: 'bet'
        """
        raise NotImplementedError()

    @property
    def sample_filters(self) -> Dict[str, Any]:
        """
        :return: A sample dictionary of filters with appropriate values
        """
        raise NotImplementedError()

    @property
    def action_cls(self) -> type(Action):
        """
        :return: The action class used to fetch data
        """
        raise NotImplementedError()

    @property
    def route_info(self) -> Tuple[str, List[str], bool]:
        """
        Provides information about the route
        :return: The path of the route,
                 A list of supported methods,
                 Whether or not the API endpoint requires authorization
        """
        return "/api/v2/{}".format(self.keyword), ["GET"], True

    def test_successful_call(self):
        """
        Tests a successful API call
        :return: None
        """
        all_results = self.decode_data(self.client.get(
            self.route_path, headers=self.generate_headers()
        ))
        self.assertEqual(all_results["status"], "ok")
        self.assertEqual(
            all_results["data"],
            jsonify_models(self.action_cls().execute())
        )

        id_result = self.decode_data(self.client.get(
            "{}/1".format(self.route_path), headers=self.generate_headers()
        ))
        self.assertEqual(id_result["status"], "ok")
        self.assertEqual(
            id_result["data"],
            jsonify_models(self.action_cls(_id=1).execute())
        )

        for key, val in self.sample_filters.items():
            filter_result = self.decode_data(self.client.get(
                "{}?{}={}".format(self.route_path, key, val),
                headers=self.generate_headers()
            ))
            self.assertEqual(filter_result["status"], "ok")
            self.assertEqual(
                filter_result["data"],
                jsonify_models(self.action_cls.from_dict(
                    {key: val}
                ).execute())
            )

    def test_unsuccessful_call(self):
        """
        Tests an unsuccessful API call
        :return: None
        """
        failed = self.decode_data(self.client.get(
            "{}/1000".format(self.route_path), headers=self.generate_headers()
        ))
        self.assertEqual(failed["status"], "error")
        self.assertEqual(failed["reason"], "ID does not exist")

        for key, val in self.sample_filters.items():

            failed = self.decode_data(self.client.get(
                "{}?{}={}&id=1".format(self.route_path, key, val),
                headers=self.generate_headers()
            ))
            self.assertEqual(failed["status"], "error")
            self.assertEqual(failed["reason"], "Can't filter specific ID")

            if key == "matchday":
                for matchday in [0, 35]:
                    failed = self.decode_data(self.client.get(
                        "{}?matchday={}".format(self.route_path, matchday),
                        headers=self.generate_headers()
                    ))
                    self.assertEqual(failed["status"], "error")
                    self.assertEqual(
                        failed["reason"], "Matchday out of bounds"
                    )
