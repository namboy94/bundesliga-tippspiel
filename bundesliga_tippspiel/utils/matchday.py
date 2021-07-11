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

from typing import Tuple
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.match_data.Match import Match


def get_matchday_info() -> Tuple[int, int]:
    """
    Retrieves information on matchdays
    :return: The current matchday as well as the maximum matchday
    """
    all_matches = Match.query.filter_by(
        season=Config.season(),
        league=Config.OPENLIGADB_LEAGUE
    ).all()
    started = [x for x in all_matches if x.has_started]
    current_matchday = max(started, key=lambda x: x.matchday).matchday
    max_matchday = max(all_matches, key=lambda x: x.matchday).matchday
    return current_matchday, max_matchday
