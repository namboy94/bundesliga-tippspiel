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
from bundesliga_tippspiel import db
from bundesliga_tippspiel.models.ModelMixin import ModelMixin


class Bet(ModelMixin, db.Model):
    """
    Model that describes the 'bets' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "bets"
    """
    The name of the table
    """

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            "users.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the user associated with this bet
    """

    user = db.relationship(
        "User", backref=db.backref("bets", lazy=True, cascade="all,delete")
    )
    """
    The user associated with this bet
    """

    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the match that this bet refers to.
    """

    match = db.relationship(
        "Match", backref=db.backref("bets", lazy=True, cascade="all,delete")
    )
    """
    The match that this bet refers to
    """

    home_score = db.Column(db.Integer, nullable=False)
    """
    The score bet on the home team
    """

    away_score = db.Column(db.Integer, nullable=False)
    """
    The score bet on the away team
    """

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "match_id": self.match_id,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "points": self.evaluate()
        }
        if include_children:
            data["user"] = self.user.__json__(include_children)
            data["match"] = self.match.__json__(include_children)
        return data

    def __repr__(self) -> str:
        """
        :return: A string with which the object may be generated
        """
        params = ""

        for key, val in self.__json__().items():
            if key == "points":
                continue
            params += "{}={}, ".format(key, repr(val))
        params = params.rsplit(",", 1)[0]

        return "{}({})".format(self.__class__.__name__, params)

    def __eq__(self, other: Any) -> bool:
        """
        Checks the model object for equality with another object
        :param other: The other object
        :return: True if the objects are equal, False otherwise
        """
        if isinstance(other, Bet):
            return self.id == other.id \
                   and self.user_id == other.user_id \
                   and self.match_id == other.match_id \
                   and self.home_score == other.home_score \
                   and self.away_score == other.away_score
        else:
            return False  # pragma: no cover

    def evaluate(self, when_finished: bool = False) -> int:
        """
        Evaluates the points score on this bet
        :param when_finished: Only calculate the value
                              when the match is finished.
                              Otherwise, returns 0
        :return: The calculated points
        """
        if when_finished and not self.match.finished:
            return 0

        points = 0
        bet_diff = self.home_score - self.away_score
        match_diff = \
            self.match.home_current_score - self.match.away_current_score

        if bet_diff == match_diff:  # Correct goal difference
            points += 5

        if bet_diff * match_diff > 0:  # Correct winner
            points += 7
        elif bet_diff == 0 and match_diff == 0:  # Draw
            points += 7

        if self.home_score == self.match.home_current_score \
                or self.away_score == self.match.away_current_score:
            points += 3

        return points
