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
from flask import render_template, request
from flask_login import login_required
from bundesliga_tippspiel import app
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
from bundesliga_tippspiel.actions.PlaceBetsAction import PlaceBetsAction


@app.route("/bets", methods=["POST", "GET"])
@app.route("/bets/<int:matchday>", methods=["GET"])
@login_required
def bets(matchday: Optional[int] = None):
    """
    Displays all matches for a matchday with entries for betting
    :param matchday: The matchday to display
    :return: None
    """
    if request.method == "GET":
        if matchday is None:
            all_matches = GetMatchAction().execute()["matches"]
            filtered = list(filter(lambda x: not x.started, all_matches))
            matchday = min(filtered, key=lambda x: x.matchday).matchday

        matchday_bets = GetBetAction(matchday=matchday).execute()["bets"]
        matchday_matches = \
            GetMatchAction(matchday=matchday).execute()["matches"]

        betmap = {}
        for match in matchday_matches:
            betmap[match.id] = None
        for bet in matchday_bets:
            betmap[bet.match.id] = bet

        return render_template(
            "bets.html",
            matchday=matchday,
            betmap=betmap,
            matches=matchday_matches
        )

    else:  # POST
        action = PlaceBetsAction.from_site_request()
        return action.execute_with_redirects(
            "bets", "Tipps erfolgreich gesetzt", "bets"
        )


@app.route("/leaderboard")
@login_required
def leaderboard():
    return render_template("index.html")
