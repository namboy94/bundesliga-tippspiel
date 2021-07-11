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
from typing import Optional
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from jerrycan.base import app
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.utils.chart_data import generate_leaderboard_data
from bundesliga_tippspiel.db.user_generated.SeasonWinner import SeasonWinner
from bundesliga_tippspiel.actions.LoadSettingsAction import LoadSettingsAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
from bundesliga_tippspiel.utils.stats import calculate_current_league_table


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/leaderboard", methods=["GET"])
    @login_required
    @action_route
    def leaderboard():
        """
        Displays a leaderboard.
        :return: The Response
        """
        start = time.time()
        settings = LoadSettingsAction().execute()

        app.logger.debug("Start generating leaderboard data")
        leaderboard_action = LeaderboardAction.from_site_request()
        leaderboard_action.include_bots = settings["display_bots"]
        leaderboard_data = leaderboard_action.execute()["leaderboard"]

        # Re-use the previously queried bets
        bets = leaderboard_action.bets
        current_matchday, leaderboard_history = generate_leaderboard_data(
            bets=bets, include_bots=settings["display_bots"]
        )

        delta = "%.2f" % (time.time() - start)
        app.logger.debug("Generated leaderboard data in {}s".format(delta))

        season_winners = {
            x.season_string: x.user_id for x in SeasonWinner.query.all()
        }

        return render_template(
            "info/../templates/tables/leaderboard.html",
            leaderboard=enumerate(leaderboard_data),
            matchday=current_matchday,
            leaderboard_history=leaderboard_history,
            show_all=True,
            season_winners=season_winners
        )

    @blueprint.route("/league_table", methods=["GET"])
    @blueprint.route("/league_table/<int:matchday>", methods=["GET"])
    @login_required
    @action_route
    def league_table(matchday: Optional[int] = None):
        """
        Calculates the current league table and displays it for the user
        :param matchday: Can be used to specify a certain matchday
        :return: The response
        """
        table = calculate_current_league_table(matchday=matchday)
        return render_template(
            "info/../templates/tables/league_table.html",
            league_table=table,
            title="Aktuelle Bundesliga Tabelle"
        )

    @blueprint.route("/user_league_table", methods=["GET"])
    @login_required
    @action_route
    def user_league_table():
        """
        Calculates the league table based on the user's bets
        :return: The response
        """
        table = calculate_current_league_table(user=current_user)
        return render_template(
            "info/../templates/tables/league_table.html",
            league_table=table,
            title=f"Tabelle nach {current_user.username}'s Tipps"
        )

    return blueprint
