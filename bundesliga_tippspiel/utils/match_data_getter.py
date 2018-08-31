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

import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
from bundesliga_tippspiel import db
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.match_data.Goal import Goal
from bundesliga_tippspiel.models.match_data.Player import Player
from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.config import openligadb_league, openligadb_season


def update_db_data(
        league: str = openligadb_league, season: str = openligadb_season
):
    """
    Updates the database with the match data for
    the specified league and season
    :param league: The league for which to update the data
    :param season: The season for which to update the data
    :return: None
    """

    # Fetch Data
    base_url = "https://www.openligadb.de/api/{}/{}/{}"
    team_data = json.loads(requests.get(
        base_url.format("getavailableteams", league, season)
    ).text)
    match_data = json.loads(requests.get(
        base_url.format("getmatchdata", league, season)
    ).text)

    matches, goals, players, teams = [], [], [], []

    # Generate Data Model Objects
    for match_data in match_data:
        match = parse_match(match_data)
        matches.append(match)

        home_score = 0
        for goal_data in match_data["Goals"]:
            goal = parse_goal(goal_data, match.id)
            if goal is None:
                continue
            goals.append(goal)

            if home_score < goal.home_score:
                team = 1
            else:
                team = -1
            if goal.own_goal:
                team *= -1
            team_id = {1: match.home_team_id, -1: match.away_team_id}[team]

            home_score = goal.home_score

            player = parse_player(goal_data, team_id)
            players.append(player)

    for team_data in team_data:
        teams.append(parse_team(team_data))

    # Store in DB
    for data, cls in [
        (teams, Team),
        (players, Player),
        (matches, Match),
        (goals, Goal)
    ]:
        store_in_db(data, cls)


def parse_match(match_data: Dict[str, Any]) -> Match:
    """
    Parses a Match object from JSON match data
    :param match_data: The match data to parse
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

    match = Match(
        id=match_data["MatchID"],
        home_team_id=match_data["Team1"]["TeamId"],
        away_team_id=match_data["Team2"]["TeamId"],
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


def parse_goal(goal_data: Dict[str, Any], match_id: int) -> Optional[Goal]:
    """
    Parses a goal JSON object and generates a Goal object
    :param match_id: The match ID of the match in which the goal was scored
    :param goal_data: The goal data to parse
    :return: The generated Goal object
    """
    if goal_data["GoalGetterID"] == 0:
        return None
    return Goal(
        id=goal_data["GoalID"],
        match_id=match_id,
        player_id=goal_data["GoalGetterID"],
        minute=goal_data["MatchMinute"],
        minute_et=None if not goal_data["IsOvertime"] else 1,  # TODO Fix
        home_score=goal_data["ScoreTeam1"],
        away_score=goal_data["ScoreTeam2"],
        own_goal=goal_data["IsOwnGoal"],
        penalty=goal_data["IsPenalty"]
    )


def parse_player(goal_data: Dict[str, Any], team_id: int) -> Player:
    """
    Parses a Player object from a Goal JSON data object
    :param goal_data: The data of a goal the player scored
    :param team_id: The Team of the player
    :return: The generated Player object
    """
    return Player(
        id=goal_data["GoalGetterID"],
        team_id=team_id,
        name=goal_data["GoalGetterName"]
    )


def parse_team(team_data: Dict[str, Any]) -> Team:
    """
    Parses team-related JSON data and generates a Team object from that
    :param team_data: The team data to parse
    :return: The generated Team object
    """
    return Team(
        id=team_data["TeamId"],
        name=team_data["TeamName"],
        abbreviation=str(team_data["TeamId"]),  # TODO Fix
        short_name=team_data["ShortName"],
        icon_png=team_data["TeamIconUrl"],  # TODO Fix
        icon_svg=team_data["TeamIconUrl"]   # TODO Fix
    )


def store_in_db(objects: List[db.Model], model_cls: type(db.Model)):
    """
    Stores a list of objects in the database. While doing so, will
    either update existing objects or create new one if they don't exist
    :param objects: The objects to add
    :param model_cls: The model class of these objects
    :return: None
    """
    existing = model_cls.query.all()
    idmap = {}
    for obj in existing:
        idmap[obj.id] = obj

    for obj in objects:
        if obj.id in idmap:
            model_cls.query.filter_by(id=obj.id).update(obj.__json__())
        else:
            db.session.add(obj)
    db.session.commit()
