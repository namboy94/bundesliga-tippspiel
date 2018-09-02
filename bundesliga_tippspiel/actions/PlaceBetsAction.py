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

from flask_login import current_user
from typing import Dict, Any, Tuple
from bundesliga_tippspiel import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.user_generated.Bet import Bet


class PlaceBetsAction(Action):
    """
    Action that allows placing bets
    """

    def __init__(self, bets: Dict[str or int, Tuple[str or int, str or int]]):
        """
        Initializes the PlaceBetsAction object
        :param bets: a dictionary mapping match IDs to tuples containing the
                     home and away scores
        :raises: ActionException if any problems occur
        """
        self.bets = bets
        self.error_count = 0

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        self.error_count = 0
        data = self.bets
        self.bets = {}

        # Filter out invalid stuff
        # noinspection PyUnresolvedReferences
        for key, value in data.items():
            try:
                match_id = int(key)
                home, away = int(value[0]), int(value[1])

                match = Match.query.get(match_id)

                if match is None:
                    raise ValueError()
                elif match.started:
                    raise ValueError()

                for score in [away, home]:
                    if not 0 <= score <= 99:
                        raise ValueError()
                self.bets[match_id] = (home, away)

            except (ValueError, TypeError, ActionException):
                self.error_count += 1
                continue

    def _execute(self) -> Dict[str, Any]:
        """
        Registers an unconfirmed user in the database
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """

        new_count = 0
        updated_count = 0

        for match_id, scores in self.bets.items():

            home, away = scores

            bet = Bet.query.filter_by(
                user_id=current_user.id,
                match_id=match_id
            ).first()

            if bet is None:
                new_count += 1
                bet = Bet(
                    user=current_user,
                    match_id=match_id,
                    home_score=home,
                    away_score=away
                )
                db.session.add(bet)
            else:
                updated_count += 1
                bet.home_score = home
                bet.away_score = away

        db.session.commit()

        return {
            "new": new_count,
            "updated": updated_count,
            "invalid": self.error_count
        }

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        bets = {}

        for key, value in data.items():
            try:
                match_id, team = key.split("-")
                match_id = int(match_id)

                if match_id not in bets:
                    bets[match_id] = (None, None)

                if team == "home":
                    bets[match_id] = (int(value), bets[match_id][1])
                elif team == "away":
                    bets[match_id] = (bets[match_id][0], int(value))
                else:
                    continue

            except (IndexError, ValueError, TypeError):
                continue

        return cls(
            bets=bets
        )
