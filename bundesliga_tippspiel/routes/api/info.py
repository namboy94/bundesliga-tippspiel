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
from typing import Optional

from flask import Blueprint, request, abort
from flask_login import login_required
from jerrycan.routes.decorators import api, api_login_required
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db import Match
from bundesliga_tippspiel.utils.collections.LeagueTable import LeagueTable
from bundesliga_tippspiel.utils.matchday import validate_matchday, \
    get_matchday_info


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)
    api_base_path = f"/api/v{Config.API_VERSION}"

    @blueprint.route(f"{api_base_path}/leagues", methods=["GET"])
    @api
    def api_get_leagues():
        """
        Retrieves a list of available leagues
        :return: The list of available leagues
        """
        return {"leagues": Config.all_leagues()}

    @blueprint.route(f"{api_base_path}/matchday_info", methods=["GET"])
    @api
    def api_matchday_info():
        """
        Retrieves the current matchday and the maximum matchday for a league
        Requires a "league" and "season" parameter in the query
        :return: The list of available leagues
        """
        current, max_matchday = get_matchday_info(
            request.args["league"], int(request.args["season"])
        )
        return {
            "current": current,
            "max": max_matchday
        }

    @blueprint.route(f"{api_base_path}/matchday/<string:league>/<int:season>",
                     methods=["GET"])
    @blueprint.route(f"{api_base_path}/matchday/"
                     f"<string:league>/<int:season>/<int:matchday>",
                     methods=["GET"])
    @api_login_required
    @login_required
    @api
    def api_matches(
            league: str,
            season: int,
            matchday: Optional[int] = None
    ):
        """
        Retrieves the matches for a particular matchday
        :return: The list of available leagues
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        matches = Match.query.filter_by(
            league=league, season=season, matchday=matchday
        ).all()
        matches.sort(key=lambda x: x.kickoff)
        matches_json = [
            match.__json__(include_children=False) for match in matches
        ]
        return {"matches": matches_json}

    @blueprint.route(f"{api_base_path}/league_table/"
                     f"<string:league>/<int:season>", methods=["GET"])
    @blueprint.route(f"{api_base_path}/league_table/"
                     f"<string:league>/<int:season>/<int:matchday>",
                     methods=["GET"])
    @api
    def api_get_league_table(
            league: str,
            season: int,
            matchday: Optional[int] = None
    ):
        """
        Retrieves a league table
        :param league: The league for which to retrieve the table
        :param season: The season for which to retrieve the table
        :param matchday: The matchday for which to retrieve the table
        :return: The leaderboard table
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        table_data = LeagueTable(league, season, matchday, None)\
            .calculate_table()
        league_table = []
        for entry in table_data:
            league_table.append((
                entry[0],
                entry[1].__json__(),
                entry[2],
                entry[3],
                entry[4],
                entry[5],
                entry[6],
                entry[7],
                entry[8],
                entry[9]
            ))

        return {
            "league_table": league_table
        }

    return blueprint
