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


class Match(db.Model):
    """
    Model that describes the 'matches' SQL table
    """

    __tablename__ = "matches"
    """
    The table name
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID of the table entries acts as a primary key
    """

    home_team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), nullable=False
    )
    """
    The ID of the home team. Acts as a foreign key
    """

    home_team = db.relationship(
        "Team", foreign_keys=[home_team_id]
    )
    """
    The home team.
    """

    away_team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), nullable=False
    )
    """
    The ID of the away team. Acts as a foreign key
    """

    away_team = db.relationship(
        "Team", foreign_keys=[away_team_id]
    )
    """
    The away team.
    """

    matchday = db.Column(db.Integer, nullable=False)
    """
    The match day of the match
    """

    home_current_score = db.Column(db.Integer)
    """
    The current score of the home team.
    """

    away_current_score = db.Column(db.Integer)
    """
    The current score of the away team.
    """

    home_ht_score = db.Column(db.Integer)
    """
    The score of the home team at half time
    """

    away_ht_score = db.Column(db.Integer)
    """
    The score of the away team at half time
    """

    home_ft_score = db.Column(db.Integer)
    """
    The final score of the home team
    """

    away_ft_score = db.Column(db.Integer)
    """
    The final score of the away team
    """

    kickoff = db.Column(db.String)
    """
    A string representing the kickoff time in UTC in the following format:
    YYYY-MM-DD:HH-mm-ss
    """

    started = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has started yet
    """

    finished = db.Column(db.Boolean, nullable=False)
    """
    Indicates whether or not the match has finished yet
    """
