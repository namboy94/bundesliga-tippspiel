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

from bundesliga_tippspiel.globals import db


class Goal(db.Model):
    """
    Model that describes the "goals" SQL table
    """

    __tablename__ = "goals"
    """
    The name of the table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID of the goal, which acts as a primary key
    """

    match_id = db.Column(
        db.Integer, db.ForeignKey("matches.id"), nullable=False
    )
    """
    The ID of the match in which this goal was scored. Acts as a foreign key.
    """

    match = db.relationship(
        "Match", backref=db.backref("goals", lazy=True)
    )
    """
    The match in which this goal was scored.
    """

    player_id = db.Column(
        db.Integer, db.ForeignKey("players.id"), nullable=False
    )
    """
    The ID of the player that scored this goal. Acts as a foreign key.
    """

    player = db.relationship(
        "Player", backref=db.backref("goals", lazy=True)
    )
    """
    The player that scored this goal.
    """

    minute = db.Column(db.Integer, nullable=False)
    """
    The minute in which the goal was scored
    """

    minute_et = db.Column(db.Integer, nullable=False)
    """
    This keeps track in which minute of extra time a goal was scored.
    """

    home_score = db.Column(db.Integer, nullable=False)
    """
    The home team's score after the goal was scored
    """

    away_score = db.Column(db.Integer, nullable=False)
    """
    The away team's score after the goal was scored
    """

    own_goal = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not this goal was an own goal
    """

    penalty = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not this goal was a penalty
    """
