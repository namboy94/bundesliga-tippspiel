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
from flask import request
from datetime import datetime
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
    max_matchday = max(all_matches, key=lambda x: x.matchday).matchday

    started = [x for x in all_matches if x.has_started]
    if len(started) == 0:
        current_matchday = 1
    else:
        now = datetime.utcnow()
        latest_match: Match = max(started, key=lambda x: x.kickoff)
        current_matchday = latest_match.matchday
        if (now - latest_match.kickoff_datetime).days >= 1:
            current_matchday = min(max_matchday, current_matchday + 1)

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
    try:
        default_league, default_season = get_selected_league()
    except RuntimeError:
        default_league, default_season = \
            Config.OPENLIGADB_LEAGUE, Config.season()

    if league is None:
        league = default_league
    if season is None:
        season = default_season
    current_matchday, max_matchday = get_matchday_info(league, season)
    if matchday is None:
        matchday = current_matchday

    if not 1 <= matchday <= max_matchday:
        return None
    else:
        return league, season, matchday


def get_selected_league() -> Tuple[str, int]:
    """
    :return: The league currently selected by the user by means of cookies
    """
    league = str(request.cookies.get("league", Config.OPENLIGADB_LEAGUE))
    try:
        season = int(request.cookies.get("season", Config.season()))
    except ValueError:
        season = Config.season()
    return league, season
