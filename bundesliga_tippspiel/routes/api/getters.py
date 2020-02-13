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

from flask import request, Blueprint
from flask_login import login_required
from typing import Optional, Dict, Any
from bundesliga_tippspiel.utils.json import jsonify_models
from bundesliga_tippspiel.utils.routes import api, api_login_required
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetPlayerAction import GetPlayerAction
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
from bundesliga_tippspiel.actions.GetEmailReminderAction import \
    GetEmailReminderAction

getters_blueprint = Blueprint("getters", __name__)


@getters_blueprint.route("/api/v2/bet", methods=["GET"])
@getters_blueprint.route("/api/v2/bet/<int:bet_id>", methods=["GET"])
@api_login_required
@login_required
@api
def get_bet(bet_id: Optional[int] = None):
    """
    Allows an authenticated user to get bet data
    :param bet_id: An optional specific ID
    :return: The results
    """
    return execute_getter(bet_id, GetBetAction)


@getters_blueprint.route("/api/v2/email_reminder", methods=["GET"])
@api_login_required
@login_required
@api
def get_email_reminder():
    """
    Allows an authenticated user to get their email reminder data
    :return: The results
    """
    return execute_getter(None, GetEmailReminderAction)


@getters_blueprint.route("/api/v2/goal", methods=["GET"])
@getters_blueprint.route("/api/v2/goal/<int:goal_id>", methods=["GET"])
@api_login_required
@login_required
@api
def get_goal(goal_id: Optional[int] = None):
    """
    Allows an authenticated user to get goal data
    :param goal_id: An optional specific ID
    :return: The results
    """
    return execute_getter(goal_id, GetGoalAction)


@getters_blueprint.route("/api/v2/match", methods=["GET"])
@getters_blueprint.route("/api/v2/match/<int:match_id>", methods=["GET"])
@api_login_required
@login_required
@api
def get_match(match_id: Optional[int] = None):
    """
    Allows an authenticated user to get match data
    :param match_id: An optional specific ID
    :return: The results
    """
    return execute_getter(match_id, GetMatchAction)


@getters_blueprint.route("/api/v2/player", methods=["GET"])
@getters_blueprint.route("/api/v2/player/<int:player_id>", methods=["GET"])
@api_login_required
@login_required
@api
def get_player(player_id: Optional[int] = None):
    """
    Allows an authenticated user to get player data
    :param player_id: An optional specific ID
    :return: The results
    """
    return execute_getter(player_id, GetPlayerAction)


@getters_blueprint.route("/api/v2/team", methods=["GET"])
@getters_blueprint.route("/api/v2/team/<int:team_id>", methods=["GET"])
@api_login_required
@login_required
@api
def get_team(team_id: Optional[int] = None):
    """
    Allows an authenticated user to get team data
    :param team_id: An optional specific ID
    :return: The results
    """
    return execute_getter(team_id, GetTeamAction)


@getters_blueprint.route("/api/v2/leaderboard", methods=["GET"])
@api_login_required
@login_required
@api
def api_leaderboard():
    """
    Enables retrieving a leaderboard
    :return: The JSON response
    """
    params = request.get_json()
    if params is None:
        params = {}
    action = LeaderboardAction().from_dict(params)
    leaderboard = action.execute()
    jsonified = jsonify_models(leaderboard, True)
    return jsonified


def execute_getter(_id: Optional[int], action_cls: type(Action)) \
        -> Dict[str, Any]:
    """
    Executes a getter API method using a Getter Action and an optional ID
    :param _id: Optional ID to use while fetching
    :param action_cls: The action class to use for fetching
    :return: The result
    """
    if _id is not None:
        return jsonify_models(action_cls(_id=_id).execute())
    else:
        action = action_cls.from_dict(request.args)
        return jsonify_models(action.execute())
