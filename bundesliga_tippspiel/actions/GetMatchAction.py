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
from bundesliga_tippspiel.models.match_data.Match import Match


class GetMatchAction(Action):
    """
    Action that enables getting Matches
    """

    def __init__(
            self,
            _id: Optional[int] = None,
            matchday: Optional[int] = None
    ):
        """
        Initializes the GetMatchAction object
        :param _id: If provided, returns the match with that ID
        :param matchday: If provided, will return all matches on that matchday
        :raises: ActionException if any problems occur
        """
        self.id = _id
        self.matchday = matchday

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        self.check_id_or_filters(self.id, [self.matchday])
        self.check_matchday_bounds(self.matchday)

    def _execute(self) -> Dict[str, Any]:
        """
        Registers an unconfirmed user in the database
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        if self.id is not None:
            result = self.handle_id_fetch(self.id, Match)

        else:

            query = Match.query

            if self.matchday is not None:
                query = query.filter_by(matchday=self.matchday)

            result = query.all()
            result.sort(key=lambda x: x.kickoff)

        return {"matches": result}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            data.get("id", None),
            data.get("matchday", None),
        )