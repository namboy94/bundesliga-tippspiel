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

from typing import Dict, Any
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.GetterApiRouteTestFramework import \
    _GetterApiRouteTestFramework


class TestGetTeamApiRoute(_GetterApiRouteTestFramework):
    """
    Tests the /team GET API route
    """

    @property
    def keyword(self) -> str:
        """
        :return: The route keyword
        """
        return "team"

    @property
    def sample_filters(self) -> Dict[str, Any]:
        """
        :return: A sample dictionary of filters with appropriate values
        """
        return {}

    @property
    def action_cls(self) -> type(Action):
        """
        :return: The action class used to fetch data
        """
        return GetTeamAction
