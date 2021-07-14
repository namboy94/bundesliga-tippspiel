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

from typing import Any, List, Optional
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.db.User import User
from bundesliga_tippspiel.db.match_data.Match import Match


class Bet(ModelMixin, db.Model):
    """
    Model that describes the 'bets' SQL table
    """

    MAX_POINTS: int = 15
    POSSIBLE_POINTS: List[int] = [0, 3, 7, 10, 12, 15]

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "bets"
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("home_team_abbreviation", "away_team_abbreviation",
             "league", "season", "matchday"),
            (Match.home_team_abbreviation, Match.away_team_abbreviation,
             Match.league, Match.season, Match.matchday)
        ),
    )

    league: str = db.Column(db.String(255), primary_key=True)
    season: int = db.Column(db.Integer, primary_key=True)
    matchday: int = db.Column(db.Integer, primary_key=True)
    home_team_abbreviation: str = db.Column(db.String(3), primary_key=True)
    away_team_abbreviation: str = db.Column(db.String(3), primary_key=True)
    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    home_score: int = db.Column(db.Integer, nullable=False)
    away_score: int = db.Column(db.Integer, nullable=False)
    points: int = db.Column(db.Integer, nullable=True)

    user: User = db.relationship(
        "User", backref=db.backref("bets", cascade="all, delete")
    )
    match: Match = db.relationship("Match", overlaps="bets")

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
            return self.user_id == other.user_id \
                   and self.home_team_abbreviation == \
                   other.home_team_abbreviation \
                   and self.away_team_abbreviation == \
                   other.away_team_abbreviation \
                   and self.home_score == other.home_score \
                   and self.away_score == other.away_score
        else:
            return False  # pragma: no cover

    def evaluate(self) -> Optional[int]:
        """
        Evaluates the current points score on this bet
        :return: The calculated points (or None if the math hasn't started yet)
        """
        if not self.match.has_started:
            return None

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
