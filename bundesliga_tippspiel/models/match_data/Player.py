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


class Player(db.Model):
    """
    Model that describes the "players" SQL table
    """

    __tablename__ = "players"
    """
    The name of the database table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID of the player is the primary key and auto-increments
    """

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    """
    The ID of the team the player is affiliated with.
    Acts as a foreign key to the 'teams' table.
    """

    team = db.relationship(
        "Team", backref=db.backref("players", lazy=True, cascade="all,delete"),
    )
    """
    The team the player is affiliated with.
    """

    name = db.Column(db.String(255), nullable=False)
    """
    The name of the player
    """
