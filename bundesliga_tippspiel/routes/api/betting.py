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

from flask import Blueprint, request
from flask_login import login_required, current_user
from jerrycan.routes.decorators import api, api_login_required
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.utils.bets import place_bets


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)
    api_base_path = f"/api/v{Config.API_VERSION}"

    @blueprint.route(f"{api_base_path}/place_bets", methods=["PUT"])
    @api_login_required
    @login_required
    @api
    def api_place_bets():
        """
        Places bets using the API
        Expects the following format:
            {
            "bets": [
                {"league": str, "season": int, "matchday": int,
                 "home_team": str, "away_team": str,
                 "home_score": int, "away_score: int}
            ]
            }
        :return: The Response
        """
        bets = [
            (x["league"], x["season"], x["matchday"],
             x["home_team"], x["away_team"],
             x["home_score"], x["away_score"])
            for x in request.get_json()["bets"]
        ]
        successful = place_bets(current_user, bets)
        return {"placed": successful}

    return blueprint
