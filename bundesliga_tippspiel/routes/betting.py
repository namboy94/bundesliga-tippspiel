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

from typing import Optional, Dict
from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from puffotter.flask.base import db
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
from bundesliga_tippspiel.actions.PlaceBetsAction import PlaceBetsAction
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.user_generated.SeasonTeamBet import \
    SeasonTeamBet, SeasonTeamBetType
from bundesliga_tippspiel.db.user_generated.SeasonPositionBet import \
    SeasonPositionBet


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/bets", methods=["POST", "GET"])
    @blueprint.route("/bets/<int:matchday>", methods=["GET"])
    @login_required
    @action_route
    def bets(matchday: Optional[int] = None):
        """
        Displays all matches for a matchday with entries for betting
        :param matchday: The matchday to display
        :return: None
        """
        if request.method == "GET":
            if matchday is None:
                matchday = -1

            matchday_bets = GetBetAction(
                matchday=matchday,
                user_id=current_user.id
            ).execute()["bets"]

            matchday_matches = GetMatchAction(
                matchday=matchday
            ).execute()["matches"]

            betmap: Dict[int, Optional[Bet]] = {}
            matchday_points = 0
            for _match in matchday_matches:
                betmap[_match.id] = None
            for bet in matchday_bets:
                betmap[bet.match.id] = bet
                matchday_points += bet.evaluate(when_finished=True)

            return render_template(
                "betting/bets.html",
                matchday=matchday_matches[0].matchday,
                betmap=betmap,
                matches=matchday_matches,
                matchday_points=matchday_points
            )

        else:  # POST
            action = PlaceBetsAction.from_site_request()
            return action.execute_with_redirects(
                "betting.bets", "Tipps erfolgreich gesetzt", "betting.bets"
            )

    @blueprint.route("/match/<int:match_id>", methods=["GET"])
    @login_required
    @action_route
    def match(match_id: int):
        """
        Displays a single match
        :param match_id: The ID of the match to display
        :return: The Response
        """
        match_info = GetMatchAction(_id=match_id).execute()["match"]
        goals_info = GetGoalAction(match_id=match_id).execute()["goals"]
        bets_info = GetBetAction(match_id=match_id).execute()["bets"]
        return render_template(
            "info/match.html",
            match=match_info,
            goals=goals_info,
            bets=bets_info
        )

    @blueprint.route("/bets/season", methods=["GET"])
    @login_required
    @action_route
    def season_bets():
        """
        Let's the user bet on season-long things.
        :return: The response
        """
        all_teams = GetTeamAction().execute()["teams"]
        season_position_bets = [
            (x.team, x)
            for x in SeasonPositionBet.query
            .filter_by(user=current_user)
            .filter_by(season=Config.season())
            .options(db.joinedload(SeasonPositionBet.team))
            .all()
        ]
        season_position_bets.sort(key=lambda x: x[1].position)
        season_positon_team_ids = [x[0].id for x in season_position_bets]
        for team in all_teams:
            if team.id not in season_positon_team_ids:
                season_position_bets.append((team, None))

        season_team_bets = [
            (x.bet_type, x)
            for x in SeasonTeamBet.query
            .filter_by(user=current_user)
            .filter_by(season=Config.season())
            .all()
        ]
        season_team_bet_types = [x[0] for x in season_team_bets]
        for bet_type in SeasonTeamBetType:
            if bet_type not in season_team_bet_types:
                season_team_bets.append((bet_type, None))
        season_team_bets.sort(key=lambda x: x[0].value)

        return render_template(
            "betting/season.html",
            all_teams=all_teams,
            team_bets=season_team_bets,
            position_bets=season_position_bets,
            closed=Action.resolve_and_check_matchday(-1) > 17
        )

    @blueprint.route("/bets/season_team_bets", methods=["POST"])
    @login_required
    @action_route
    def place_season_team_bets():
        """
        Let's the user bet on season-long things.
        :return: The response
        """
        if Action.get_current_matchday() > 17:
            flash("Saisonübergreifende Wetten können nur vor dem 18. "
                  "Spieltag abgeschlossen werden", "danger")
            return redirect(url_for("betting.season_bets"))

        existing_team_bets = {
            x.bet_type: x
            for x in SeasonTeamBet.query
            .filter_by(user=current_user)
            .filter_by(season=Config.season())
            .all()
        }
        teams = {x.id: x for x in GetTeamAction().execute()["teams"]}

        for bet_type in SeasonTeamBetType:
            bet_value = request.form.get(bet_type.name, "")
            if not bet_value.isdigit():
                continue

            team_id = int(bet_value)
            if team_id not in teams:
                continue

            team = teams[team_id]

            bet = existing_team_bets.get(bet_type)
            if bet is None:
                bet = SeasonTeamBet(
                    bet_type=bet_type, user=current_user,
                    season=Config.season()
                )
                db.session.add(bet)
            bet.team = team

        db.session.commit()

        return redirect(url_for("betting.season_bets"))

    @blueprint.route("/bets/season_position_bets", methods=["POST"])
    @login_required
    @action_route
    def place_season_position_bets():
        """
        Let's the user bet on season-long things.
        :return: The response
        """
        if Action.get_current_matchday() > 17:
            flash("Saisonübergreifende Wetten können nur vor dem 18. "
                  "Spieltag abgeschlossen werden", "danger")
            return redirect(url_for("betting.season_bets"))

        existing_bets = {
            x.team_id: x
            for x in SeasonPositionBet.query
            .filter_by(user=current_user)
            .filter_by(season=Config.season())
            .all()
        }

        for team in GetTeamAction().execute()["teams"]:
            team_position = request.form.get(str(team.id), "")
            if not team_position.isdigit():
                continue

            if team.id in existing_bets:
                bet = existing_bets[team.id]
            else:
                bet = SeasonPositionBet(
                    user=current_user, team=team, season=Config.season()
                )
                db.session.add(bet)
            bet.position = int(team_position)

        db.session.commit()

        return redirect(url_for("betting.season_bets"))

    return blueprint
