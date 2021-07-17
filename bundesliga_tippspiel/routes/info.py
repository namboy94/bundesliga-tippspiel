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
from jerrycan.base import db
from flask import render_template, Blueprint, abort
from flask_login import login_required, current_user
from jerrycan.db.User import User

from bundesliga_tippspiel.db import Team, Player, DisplayBotsSettings, \
    Bet, Match, UserProfile


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/team/<string:team_abbreviation>")
    @login_required
    def team(team_abbreviation: int):
        """
        Displays information about a single team
        :param team_abbreviation: The ID of the team to display
        :return: The response
        """
        team_info = Team.query.filter_by(
            abbreviation=team_abbreviation
        ).options(db.joinedload(Team.players)
                  .subqueryload(Player.goals)).first()
        if team_info is None:
            return abort(404)

        recent_matches = [x for x in team_info.matches if x.finished]
        recent_matches.sort(key=lambda x: x.kickoff)
        recent_matches = recent_matches[-7:]

        match_data = []
        for match_item in recent_matches:
            if match_item.home_team_abbreviation == team_abbreviation:
                opponent = match_item.away_team
                own_score = match_item.home_current_score
                opponent_score = match_item.away_current_score
            else:
                opponent = match_item.home_team
                own_score = match_item.away_current_score
                opponent_score = match_item.home_current_score

            if own_score > opponent_score:
                result = "win"
            elif own_score < opponent_score:
                result = "loss"
            else:
                result = "draw"

            score = "{}:{}".format(own_score, opponent_score)
            match_data.append((
                match_item, opponent, score, result
            ))

        goal_data = []
        for player in team_info.players:
            goals = [x for x in player.goals if not x.own_goal]
            goal_data.append((player.name, len(goals)))
        goal_data.sort(key=lambda x: x[1], reverse=True)

        return render_template(
            "info/team.html",
            team=team_info,
            goals=goal_data,
            matches=match_data
        )

    @blueprint.route("/match/<string:league>/<int:season>/"
                     "<int:matchday>/<string:matchup>",
                     methods=["GET"])
    @login_required
    def match(league: str, season: int, matchday: int, matchup: str):
        """
        Displays a single match
        :param league: The league of the match
        :param season: The season of the match
        :param matchday: The matchday of the match
        :param matchup: The matchup string ('hometeam_awayteam')
        :return: The Response
        """
        try:
            home, away = matchup.split("_")
            match_item = Match.query.filter_by(
                league=league,
                season=season,
                matchday=matchday,
                home_team_abbreviation=home,
                away_team_abbreviation=away
            ).options(db.joinedload(Match.goals)).first()
            if match_item is None:
                raise ValueError()
        except ValueError:
            return abort(404)

        bets: List[Bet] = Bet.query.filter_by(
            league=league,
            season=season,
            matchday=matchday,
            home_team_abbreviation=home,
            away_team_abbreviation=away
        ).options(db.joinedload(Bet.user)
                  .subqueryload(User.profile)
                  .subqueryload(UserProfile.favourite_team)).all()
        if not DisplayBotsSettings.get_state(current_user):
            bets = [
                x for x in bets
                if DisplayBotsSettings.bot_symbol() not in x.user.username
            ]
        bets.sort(key=lambda x: x.user_id)
        if match_item.has_started:
            bets.sort(key=lambda x: x.points, reverse=True)

        return render_template(
            "info/match.html",
            match=match_item,
            bets=bets
        )

    return blueprint
