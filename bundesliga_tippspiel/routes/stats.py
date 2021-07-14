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
from flask import render_template, abort, Blueprint
from flask_login import login_required, current_user
from jerrycan.db.User import User
from bundesliga_tippspiel.db import DisplayBotsSettings
from bundesliga_tippspiel.utils.matchday import validate_matchday
from bundesliga_tippspiel.utils.collections.StatsGenerator import \
    StatsGenerator
from bundesliga_tippspiel.utils.collections.UserStatsGenerator import \
    UserStatsGenerator


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/user/<int:user_id>")
    @blueprint.route("/user/<int:user_id>/"
                     "<string:league>/<int:season>/<int:matchday>")
    @login_required
    def user(
            user_id: int,
            league: Optional[str] = None,
            season: Optional[int] = None,
            matchday: Optional[int] = None
    ):
        """
        Shows a page describing a user + statistics
        :param league: The league to display
        :param season: The season to display
        :param matchday: The matchday to display
        :param user_id: The ID of the user to display
        :return: The request response
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        user_data = User.query.get(user_id)
        if user_data is None:
            return abort(404)
        show_bots = DisplayBotsSettings.get_state(current_user) or \
            DisplayBotsSettings.bot_symbol() in user_data.username

        user_stats = UserStatsGenerator(
            league, season, matchday, user_data, show_bots
        )

        return render_template(
            "stats/user.html",
            user=user_data,
            user_stats=user_stats
        )

    @blueprint.route("/stats", methods=["GET"])
    @blueprint.route("/stats/"
                     "<string:league>/<int:season>/<int:matchday>")
    @login_required
    def stats(
            league: Optional[str] = None,
            season: Optional[int] = None,
            matchday: Optional[int] = None,
    ):
        """
        Displays various global statistics
        :param league: The league to display
        :param season: The season to display
        :param matchday: The matchday to display
        :return: None
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        show_bots = DisplayBotsSettings.get_state(current_user)
        global_stats = StatsGenerator(league, season, matchday, show_bots)

        return render_template(
            "stats/stats.html",
            stats=global_stats
        )

    return blueprint
