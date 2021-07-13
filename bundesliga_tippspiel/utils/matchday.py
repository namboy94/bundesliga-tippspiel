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

from typing import Tuple, Optional
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.match_data.Match import Match


def get_matchday_info(league: str, season: int) -> Tuple[int, int]:
    """
    Retrieves information on matchdays
    :param league: The league for which to retrieve the information
    :param season: The season for which to retrieve the information
    :return: The current matchday as well as the maximum matchday
    """
    all_matches = Match.query.filter_by(
        season=season,
        league=league
    ).all()
    started = [x for x in all_matches if x.has_started]
    current_matchday = max(started, key=lambda x: x.matchday).matchday
    max_matchday = max(all_matches, key=lambda x: x.matchday).matchday
    return current_matchday, max_matchday


def validate_matchday(
        league: Optional[str],
        season: Optional[int],
        matchday: Optional[int]
) -> Optional[Tuple[str, int, int]]:
    """
    Performs checks that a league/season/matchday combination is valid.
    Can also fill these values with default values
    :param league: The league to check
    :param season: The season to check
    :param matchday: The matchday to check
    :return: league, season, matchday if valid, None if invalid
    """
    if league is None:
        league = Config.OPENLIGADB_LEAGUE
    if season is None:
        season = Config.season()
    current_matchday, max_matchday = get_matchday_info(league, season)
    if matchday is None:
        matchday = current_matchday

    if not 1 <= matchday <= max_matchday:
        return None
    else:
        return league, season, matchday
