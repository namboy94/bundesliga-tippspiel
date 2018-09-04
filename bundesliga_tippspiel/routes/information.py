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
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction


@app.route("/leaderboard", methods=["GET"])
@login_required
def leaderboard():
    """
    Displays a leaderboard.
    :return: The Response
    """
    leaderboard_data = \
        LeaderboardAction.from_site_request().execute()["leaderboard"]
    return render_template(
        "leaderboard.html",
        leaderboard=enumerate(leaderboard_data)
    )


@app.route("/team/<int:team_id>")
@login_required
def team(team_id: int):
    """
    Displays information about a single team
    :param team_id: The ID of the team to display
    :return: The response
    """
    team_info = GetTeamAction(_id=team_id).execute()["team"]
    return render_template("team.html", team=team_info)
