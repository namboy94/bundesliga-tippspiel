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

from typing import Union
from flask import render_template, abort, Blueprint
from flask_login import login_required
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.utils.chart_data import generate_leaderboard_data
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.LoadSettingsAction import LoadSettingsAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
from bundesliga_tippspiel.utils.stats import get_team_points_data, \
    generate_team_points_table, get_total_points_per_team, \
    generate_points_distributions, create_participation_ranking, \
    create_point_average_ranking


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/user/<int:user_id>")
    @login_required
    @action_route
    def user(user_id: int):
        """
        Shows a page describing a user/
        :param user_id: The ID of the user to display
        :return: The request response
        """
        settings = LoadSettingsAction().execute()
        user_data = User.query.get(user_id)
        if user_data is not None and "🤖" in user_data.username:
            # If the user to display is a bot, show other bots as well
            settings["display_bots"] = True

        if user_data is None:
            abort(404)

        bets = Bet.query.join(Match)\
            .filter(Match.season == Config.season())\
            .all()
        total_bets = len(list(filter(lambda x: x.user_id == user_id, bets)))
        bets = list(filter(lambda x: x.match.finished, bets))
        rr_bets = list(filter(lambda x: x.match.matchday > 17, bets))

        current_matchday, leaderboard_history = generate_leaderboard_data(
            bets=bets, include_bots=settings["display_bots"]
        )
        _, rr_history = generate_leaderboard_data(
            bets=rr_bets, include_bots=settings["display_bots"]
        )

        bets = list(filter(lambda x: x.user_id == user_id, bets))

        total_points = 0
        for bet in bets:
            total_points += bet.evaluate(True)

        _team_points = get_team_points_data(bets)[user_data]
        team_points = generate_team_points_table(_team_points)

        points_distribution = generate_points_distributions(bets)[user_data]
        average_points = create_point_average_ranking(bets)[0][1]
        participation = create_participation_ranking(bets)[0][1]

        placements = leaderboard_history[user_data.username][1]
        rr_placements = rr_history[user_data.username][1]
        current_placement: Union[str, int] = "N/A"
        if len(placements) >= 1:
            current_placement = placements[len(placements) - 1]
        if len(placements) >= 17:
            hinrunde_placement = placements[16]
        else:
            hinrunde_placement = placements[-1]
        ruckrunde_placement: Union[str, int] = "N/A"
        if len(rr_placements) >= 17:
            ruckrunde_placement = rr_placements[-1]

        return render_template(
            "info/../templates/stats/user.html",
            user=user_data,
            leaderboard_history=leaderboard_history,
            matchday=current_matchday,
            team_points=enumerate(team_points),
            points_distribution=points_distribution,
            player_points=total_points,
            player_bet_count=total_bets,
            player_avg_points=average_points,
            player_participation=participation,
            player_correct_bets_count=points_distribution.get(15, 0),
            player_incorrect_bets_count=points_distribution.get(0, 0),
            player_best_team=(team_points[0]),
            player_worst_team=team_points[len(team_points) - 1],
            player_current_placement=current_placement,
            player_hinrunde_placement=hinrunde_placement,
            player_ruckrunde_placement=ruckrunde_placement,
            player_best_placement=min(placements),
            player_worst_placement=max(placements)
        )

    @blueprint.route("/stats", methods=["GET"])
    @login_required
    @action_route
    def stats():
        """
        Displays a statistics page.
        :return: The Response
        """
        bets = [
            x for x in
            Bet.query
            .options(
                db.joinedload(Bet.match).subqueryload(Match.home_team)
            )
            .options(
                db.joinedload(Bet.match).subqueryload(Match.away_team)
            )
            .options(db.joinedload(Bet.user))
            .all()
            if x.match.season == Config.season()
        ]
        finished_bets = list(filter(lambda x: x.match.finished, bets))
        settings = LoadSettingsAction().execute()

        leaderboards = []
        for _filter, bets_data, count in [
            (lambda x: x.match.matchday <= 17, bets, False),
            (lambda x: x.match.matchday > 17, bets, False),
            (lambda x: x.evaluate() == 15, finished_bets, True),
            (lambda x: x.evaluate() == 0, finished_bets, True)
        ]:
            dataset = list(filter(_filter, bets_data))

            leaderboard_action = LeaderboardAction(
                34, count, settings["display_bots"], dataset
            )
            leaderboards.append(leaderboard_action.execute()["leaderboard"])

        team_points = get_total_points_per_team(finished_bets)
        team_points = generate_team_points_table(team_points)

        points_distribution = {}
        for _, distrib in generate_points_distributions(finished_bets).items():
            for key, value in distrib.items():
                if key not in points_distribution:
                    points_distribution[key] = 0
                points_distribution[key] += value

        participation_ranking = create_participation_ranking(
            finished_bets, settings["display_bots"]
        )
        average_ranking = create_point_average_ranking(
            finished_bets, settings["display_bots"]
        )

        return render_template(
            "info/../templates/stats/stats.html",
            first_leaderboard=enumerate(leaderboards[0]),
            second_leaderboard=enumerate(leaderboards[1]),
            max_leaderboard=enumerate(leaderboards[2]),
            zero_leaderboard=enumerate(leaderboards[3]),
            team_points=enumerate(team_points),
            points_distribution=points_distribution,
            participation_ranking=enumerate(participation_ranking),
            average_ranking=enumerate(average_ranking),
            show_all=True
        )

    return blueprint
