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

from flask import render_template
from flask_login import login_required
from bundesliga_tippspiel import app
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetPlayerAction import GetPlayerAction
from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction


@app.route("/leaderboard", methods=["GET"])
@login_required
@action_route
def leaderboard():
    """
    Displays a leaderboard.
    :return: The Response
    """
    leaderboard_data = \
        LeaderboardAction.from_site_request().execute()["leaderboard"]
    return render_template(
        "info/leaderboard.html",
        leaderboard=enumerate(leaderboard_data)
    )


@app.route("/team/<int:team_id>")
@login_required
@action_route
def team(team_id: int):
    """
    Displays information about a single team
    :param team_id: The ID of the team to display
    :return: The response
    """
    team_data = GetTeamAction(_id=team_id).execute()["team"]

    matches = GetMatchAction(team_id=team_id).execute()["matches"]
    matches = list(filter(lambda x: x.finished, matches))[-5:]
    match_data = []

    for match in matches:
        if match.home_team.id == team_id:
            opponent = match.away_team
            own_score = match.home_current_score
            opponent_score = match.away_current_score
        else:
            opponent = match.home_team
            own_score = match.away_current_score
            opponent_score = match.home_current_score

        if own_score > opponent_score:
            result = "win"
        elif own_score < opponent_score:
            result = "loss"
        else:
            result = "draw"

        score = "{}:{}".format(own_score, opponent_score)
        match_data.append((opponent.id, opponent.short_name, score, result))

    players = GetPlayerAction(team_id=team_id).execute()["players"]

    goal_data = []
    for player in players:
        player_goals = GetGoalAction(player_id=player.id).execute()["goals"]
        player_goals = list(filter(lambda x: not x.own_goal, player_goals))
        goal_data.append((player.name, len(player_goals)))
    goal_data.sort(key=lambda x: x[1], reverse=True)

    return render_template(
        "info/team.html",
        team=team_data,
        goals=goal_data,
        matches=match_data
    )
