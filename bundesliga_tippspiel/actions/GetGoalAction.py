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

from typing import Dict, Any, Optional
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.models.match_data.Goal import Goal


class GetGoalAction(Action):
    """
    Action that allows retrieving goals from the database
    """

    def __init__(
            self,
            _id: Optional[int] = None,
            matchday: Optional[int] = None,
            match_id: Optional[int] = None,
            player_id: Optional[int] = None,
            team_id: Optional[int] = None
    ):
        """
        Initializes the GetGoalAction object
        :param _id: If provided, returns the goal with the specified ID
        :param matchday: If provided, will only fetch goals
                         on the specified matchday
        :param match_id: If provided, will only fetch goals that occured
                         during the specified match
        :param player_id: If provided, will only fetch goals from
                          the specified player
        :param team_id: If provided, will only fetch goals from
                        the specified team
        :raises: ActionException if any problems occur
        """
        self.id = None if _id is None else int(_id)
        self.matchday = None if matchday is None else int(matchday)
        self.match_id = None if match_id is None else int(match_id)
        self.player_id = None if player_id is None else int(player_id)
        self.team_id = None if team_id is None else int(team_id)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        self.check_id_or_filters(
            self.id,
            [self.matchday, self.match_id, self.player_id, self.team_id]
        )
        self.matchday = self.resolve_and_check_matchday(self.matchday)

    def _execute(self) -> Dict[str, Any]:
        """
        Registers an unconfirmed user in the database
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        if self.id is not None:
            result = [self.handle_id_fetch(self.id, Goal)]

        else:

            query = Goal.query

            if self.matchday is not None:
                query = query.filter(Goal.match.has(matchday=self.matchday))
            if self.match_id is not None:
                query = query.filter_by(match_id=self.match_id)
            if self.player_id is not None:
                query = query.filter_by(player_id=self.player_id)
            if self.team_id is not None:
                query = query.filter(Goal.player.has(team_id=self.team_id))

            result = query.all()
            result.sort(key=lambda x: x.match.kickoff)

        return self.prepare_get_response(result, "goal")

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            _id=data.get("id"),
            matchday=data.get("matchday"),
            match_id=data.get("match_id"),
            team_id=data.get("team_id"),
            player_id=data.get("player_id")
        )
