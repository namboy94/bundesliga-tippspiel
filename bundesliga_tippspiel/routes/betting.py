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

from typing import List

from bundesliga_tippspiel.utils.collections.Leaderboard import Leaderboard
from flask import render_template, request, Blueprint, flash, url_for, \
    redirect, abort
from flask_login import login_required, current_user
from jerrycan.base import db
from bundesliga_tippspiel.db import Match, DisplayBotsSettings
from bundesliga_tippspiel.utils.matchday import validate_matchday
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.utils.bets import place_bets as _place_bets


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/bets", methods=["GET"])
    @login_required
    def get_current_bets():
        """
        Displays all matches for the current matchday with entries for betting.
        :return: The response
        """
        league, season, matchday = validate_matchday(None, None, None)
        return get_bets(league, season, matchday)

    @blueprint.route("/bets/<string:league>/<int:season>/<int:matchday>",
                     methods=["GET"])
    @login_required
    def get_bets(league: str, season: int, matchday: int):
        """
        Displays all matches for a matchday with entries for betting
        :param league: The league to display
        :param season: The season to display
        :param matchday: The matchday to display
        :return: The response
        """
        validated = validate_matchday(league, season, matchday)
        if validated is None:
            return abort(404)
        league, season, matchday = validated

        matches: List[Match] = Match.query.filter_by(
            matchday=matchday,
            season=season,
            league=league
        ).options(
            db.joinedload(Match.home_team),
            db.joinedload(Match.away_team)
        ).all()
        if len(matches) == 0:
            flash("Den angegebenen Spieltag gibt es nicht", "danger")
            return redirect(url_for("bets.get_bets"))
        matches.sort(key=lambda x: x.kickoff)
        has_started = matches[0].has_started
        all_started = matches[-1].has_started

        bets = Bet.query.filter_by(
            matchday=matchday,
            season=season,
            league=league,
            user_id=current_user.id
        ).all()

        matchday_points = 0
        for bet in bets:
            if bet.points is not None:
                matchday_points += bet.points

        bet_match_map = {
            (x.home_team_abbreviation, x.away_team_abbreviation): x
            for x in bets
        }

        bet_infos = []
        for match_item in matches:
            index = (
                match_item.home_team_abbreviation,
                match_item.away_team_abbreviation
            )
            bet_infos.append((match_item, bet_match_map.get(index)))

        leaderboard = None
        if has_started:
            leaderboard = Leaderboard(
                league,
                season,
                matchday,
                DisplayBotsSettings.get_state(current_user)
            )

        return render_template(
            "betting/bets.html",
            matchday=matchday,
            season=season,
            league=league,
            bet_infos=bet_infos,
            matchday_points=matchday_points,
            has_started=has_started,
            all_started=all_started,
            leaderboard=leaderboard
        )

    @blueprint.route("/bets", methods=["POST"])
    @login_required
    def place_bets():
        """
        Places bets for a user
        Form data should be in the format:
            {'league_season_hometeam_awayteam': 'homescore_awayscore'}
        :return: The response
        """
        bet_data = {}
        for identifier, value in request.form.items():
            try:
                league, _season, day, home, away, mode = identifier.split("_")
                season = int(_season)
                matchday = int(day)
                score = int(value)
                id_tuple = (league, season, matchday, home, away)
                if id_tuple not in bet_data:
                    bet_data[id_tuple] = {}
                bet_data[id_tuple][mode] = score
            except ValueError:
                continue

        bets = []
        for (league, season, matchday, home, away), scores in bet_data.items():
            if "home" not in scores or "away" not in scores:
                continue
            else:
                bets.append((
                    league, season, matchday,
                    home, away, scores["home"], scores["away"]
                ))
        _place_bets(current_user, bets)
        flash("Tipps erfolgreich gesetzt", "success")
        return redirect(url_for("betting.get_current_bets"))

    return blueprint
