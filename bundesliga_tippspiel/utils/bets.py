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

from typing import List, Tuple
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.db import Match, Bet


def place_bets(
        user: User,
        bets: List[Tuple[str, int, int, str, str, int, int]]
) -> List[Tuple[str, int, int, str, str, int, int]]:
    """
    Places bets for a user
    :param user: The betting user
    :param bets: The bets to place in the form
                    (league, season, matchday, home_abbrv, away_abbrv,
                     home_score, away_score)
    :return: A list of successful bets
    """
    successful = []
    matches = {
        (x.home_team_abbreviation, x.away_team_abbreviation): x
        for x in Match.query.all()
    }
    for bet_tuple in bets:
        league, season, matchday, home, away, home_score, away_score = \
            bet_tuple
        match = matches.get((home, away))
        if match is None or match.has_started:
            continue  # Can't bet on started matches
        bet = Bet(
            league=league,
            season=season,
            matchday=matchday,
            home_team_abbreviation=home,
            away_team_abbreviation=away,
            user_id=user.id,
            home_score=home_score,
            away_score=away_score
        )
        db.session.merge(bet)
        successful.append(bet_tuple)
    db.session.commit()
    return successful
