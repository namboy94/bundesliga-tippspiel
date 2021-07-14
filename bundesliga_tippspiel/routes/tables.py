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
from flask import render_template, Blueprint, request, abort
from flask_login import login_required, current_user
from bundesliga_tippspiel.db import DisplayBotsSettings
from bundesliga_tippspiel.utils.collections.Leaderboard import Leaderboard
from bundesliga_tippspiel.utils.collections.LeagueTable import LeagueTable
from bundesliga_tippspiel.utils.matchday import validate_matchday


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/leaderboard", methods=["GET"])
    @blueprint.route(
        "/leaderboard/<string:league>/<int:season>/<int:matchday>",
        methods=["GET"]
    )
    @login_required
    def leaderboard(
            league: Optional[str] = None,
            season: Optional[int] = None,
            matchday: Optional[int] = None
    ):
        """
        Displays a leaderboard.
        :param league: The league for which to display the leaderboard
        :param season: The season for which to display the leaderboard
        :param matchday: The matchday for which to display the leaderboard
        :return: The Response
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        matchday_leaderboard = Leaderboard(
            league,
            season,
            matchday,
            DisplayBotsSettings.get_state(current_user)
        )

        return render_template(
            "ranking/leaderboard.html",
            leaderboard=matchday_leaderboard
        )

    @blueprint.route("/league_table", methods=["GET"])
    @blueprint.route("/league_table/<string:league>/<int:season>/"
                     "<int:matchday>", methods=["GET"])
    @login_required
    def league_table(
            league: Optional[str] = None,
            season: Optional[int] = None,
            matchday: Optional[int] = None
    ):
        """
        Calculates the current league table and displays it for the user.
        Can also show a league table based on a user's bets if the
        GET parameter 'use_bets' is set to 1
        :param league: The league to display
        :param season: The season to display
        :param matchday: The matchday to display
        :return: The response
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        user = None
        title = "Aktuelle Ligatabelle"
        if request.args.get("use_bets") == "1":
            user = current_user
            title = f"Tabelle nach {current_user.username}'s Tipps"

        table = LeagueTable(league, season, matchday, user)
        return render_template(
            "info/league_table.html",
            league_table=table,
            title=title
        )

    return blueprint
