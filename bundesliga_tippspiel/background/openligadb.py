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

import time
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from jerrycan.base import db, app
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Goal import Goal
from bundesliga_tippspiel.db.match_data.Player import Player
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.utils.teams import get_team_data


class UpdateTracker:
    """
    Class that keeps track of OpenLigaDB updates, which is useful to avoid
    rate limiting
    """
    UPDATES: Dict[Tuple[str, int], int] = {}

    @staticmethod
    def update_required(league: str, season: int) -> bool:
        """
        Checks if a league requires updating
        :param league: The league to check
        :param season: The season to check
        :return: True if update required, False otherwise
        """
        league_tuple = (league, season)
        last_update = UpdateTracker.UPDATES.get(league_tuple, 0)

        if last_update == 0:
            return True  # Update on startup

        now = datetime.utcnow()
        delta = time.time() - last_update

        matches: List[Match] = Match.query.filter_by(
            season=season, league=league
        ).all()
        unfinished_matches = [x for x in matches if not x.finished]

        if len(matches) == 0:  # Initial filling of DB
            return True

        unfinished_matches.sort(key=lambda x: x.kickoff)
        # Don't update after the season ends
        if len(unfinished_matches) == 0:
            return False

        started_matches = [
            match for match in unfinished_matches
            if match.has_started
        ]
        is_primary = \
            league_tuple == (Config.OPENLIGADB_LEAGUE, Config.season())

        if delta > 60 * 60 * 24:  # Once a day minimum update
            return True
        elif is_primary and delta > 60 * 60:
            # Update Primary league once an hour
            return True
        elif len(started_matches) > 0:
            last_started_match = started_matches[-1]
            last_started_delta = last_started_match.kickoff_datetime - now
            last_started_seconds_delta = last_started_delta.seconds
            # Increase update frequency during and after matches
            if last_started_seconds_delta < 60 * 180:
                return True
            else:
                return False
        else:
            return False


def update_openligadb():
    """
    Updates all OpenLigaDB leagues in the configuration
    :return: None
    """
    start = time.time()
    app.logger.debug("Updating OpenLigaDB data")
    for league, season in Config.all_leagues():
        update_required = UpdateTracker.update_required(league, season)
        if update_required:
            UpdateTracker.UPDATES[(league, season)] = int(time.time())
            update_match_data(league, str(season))
    app.logger.debug(
        f"Finished OpenLigaDB update in {time.time() - start:.2f}s"
    )


def update_match_data(
        league: Optional[str] = None,
        season: Optional[str] = None
):
    """
    Updates the database with the match data for
    the specified league and season using openligadb data
    :param league: The league for which to update the data
    :param season: The season for which to update the data
    :return: None
    """
    app.logger.info(f"Updating match data for {league}/{season}")

    if league is None:
        league = Config.OPENLIGADB_LEAGUE
    if season is None:
        season = Config.OPENLIGADB_SEASON

    # Fetch Data
    base_url = "https://www.openligadb.de/api/{}/{}/{}"
    try:
        team_data = json.loads(requests.get(
            base_url.format("getavailableteams", league, season)
        ).text)
        match_data = json.loads(requests.get(
            base_url.format("getmatchdata", league, season)
        ).text)
    except (ConnectionError, requests.exceptions.ReadTimeout):
        app.logger.warning("Failed to update match data due to failed request")
        return

    for team_info in team_data:
        team = parse_team(team_info)
        db.session.merge(team)

    for match_info in match_data:
        match = parse_match(match_info, league, int(season))
        match = db.session.merge(match)

        home_score = 0
        for goal_data in match_info["Goals"]:
            goal = parse_goal(goal_data, match)
            if goal is None:
                continue

            if home_score < goal.home_score:
                goal_team = 1
            else:
                goal_team = -1
            if goal.own_goal:
                goal_team *= -1

            team_abbreviation = {
                1: match.home_team_abbreviation,
                -1: match.away_team_abbreviation
            }[goal_team]

            goal.player_team_abbreviation = team_abbreviation
            home_score = goal.home_score
            player = parse_player(goal_data, team_abbreviation)

            db.session.merge(player)
            db.session.merge(goal)

    db.session.commit()


def parse_match(match_data: Dict[str, Any], league: str, season: int) -> Match:
    """
    Parses a Match object from JSON match data
    :param match_data: The match data to parse
    :param league: The league
    :param season: The season
    :return: The generated Match object
    """
    ht_home = 0
    ht_away = 0
    ft_home = 0
    ft_away = 0

    for result in match_data["MatchResults"]:
        if result["ResultName"] == "Halbzeit":
            ht_home = result["PointsTeam1"]
            ht_away = result["PointsTeam2"]
        elif result["ResultName"] == "Endergebnis":
            ft_home = result["PointsTeam1"]
            ft_away = result["PointsTeam2"]
        else:  # pragma: no cover
            pass
    cur_home = max(ht_home, ft_home)
    cur_away = max(ht_away, ft_away)

    kickoff = match_data["MatchDateTimeUTC"]
    kickoff = datetime.strptime(kickoff, "%Y-%m-%dT%H:%M:%SZ")
    started = datetime.utcnow() > kickoff
    kickoff = kickoff.strftime("%Y-%m-%d:%H-%M-%S")

    home_team_abbreviation = get_team_data(match_data["Team1"]["TeamName"])[2]
    away_team_abbreviation = get_team_data(match_data["Team2"]["TeamName"])[2]

    match = Match(
        home_team_abbreviation=home_team_abbreviation,
        away_team_abbreviation=away_team_abbreviation,
        season=season,
        league=league,
        matchday=match_data["Group"]["GroupOrderID"],
        home_current_score=cur_home,
        away_current_score=cur_away,
        home_ht_score=ht_home,
        away_ht_score=ht_away,
        home_ft_score=ft_home,
        away_ft_score=ft_away,
        kickoff=kickoff,
        started=started,
        finished=match_data["MatchIsFinished"]
    )
    return match


def parse_goal(goal_data: Dict[str, Any], match: Match) -> Optional[Goal]:
    """
    Parses a goal JSON object and generates a Goal object
    :param match: The match in which the goal was scored
    :param goal_data: The goal data to parse
    :return: The generated Goal object
    """
    if goal_data["GoalGetterID"] == 0:
        return None

    minute = goal_data["MatchMinute"]

    # Minute defaults to 0 in case the minute data is missing.
    # This keeps the entire thing from imploding.
    if minute is None:
        minute = 0

    minute_et = 0
    if minute > 90:
        minute_et = minute - 90
        minute = 90

    goal = Goal(
        home_team_abbreviation=match.home_team_abbreviation,
        away_team_abbreviation=match.away_team_abbreviation,
        season=match.season,
        league=match.league,
        matchday=match.matchday,
        player_name=goal_data["GoalGetterName"],
        player_team_abbreviation=None,
        minute=minute,
        minute_et=minute_et,
        home_score=goal_data["ScoreTeam1"],
        away_score=goal_data["ScoreTeam2"],
        own_goal=goal_data["IsOwnGoal"],
        penalty=goal_data["IsPenalty"]
    )

    if goal.home_score == 0 and goal.away_score == 0:
        return None
    else:
        return goal


def parse_player(goal_data: Dict[str, Any], team_abbreviation: str) -> Player:
    """
    Parses a Player object from a Goal JSON data object
    :param goal_data: The data of a goal the player scored
    :param team_abbreviation: The Team of the player
    :return: The generated Player object
    """
    return Player(
        team_abbreviation=team_abbreviation,
        name=goal_data["GoalGetterName"]
    )


def parse_team(team_data: Dict[str, Any]) -> Team:
    """
    Parses team-related JSON data and generates a Team object from that
    :param team_data: The team data to parse
    :return: The generated Team object
    """
    name, short_name, abbrev, icons = get_team_data(team_data["TeamName"])
    svg, png = icons
    return Team(
        name=name,
        abbreviation=abbrev,
        short_name=short_name,
        icon_svg=svg,
        icon_png=png
    )
