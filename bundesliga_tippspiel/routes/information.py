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
from flask import render_template, abort
from flask_login import login_required
from bundesliga_tippspiel import app
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.utils.chart_data import generate_leaderboard_data
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.GetTeamAction import GetTeamAction
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetPlayerAction import GetPlayerAction
from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
from bundesliga_tippspiel.utils.stats import get_team_points_data, \
    generate_team_points_table, get_total_points_per_team, \
    generate_points_distributions, create_participation_ranking, \
    create_point_average_ranking


@app.route("/leaderboard", methods=["GET"])
@login_required
@action_route
def leaderboard():
    """
    Displays a leaderboard.
    :return: The Response
    """
    start = time.time()

    app.logger.debug("Start generating leaderboard data")
    leaderboard_action = LeaderboardAction.from_site_request()
    leaderboard_data = leaderboard_action.execute()["leaderboard"]

    # Re-use the previously queried bets
    bets = leaderboard_action.bets
    current_matchday, leaderboard_history = \
        generate_leaderboard_data(bets=bets)

    delta = "%.2f" % (time.time() - start)
    app.logger.debug("Generated leaderboard data in {}s".format(delta))

    return render_template(
        "info/leaderboard.html",
        leaderboard=enumerate(leaderboard_data),
        matchday=current_matchday,
        leaderboard_history=leaderboard_history,
        show_all=True,
        charts=True
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
        match_data.append((
            opponent.id, opponent.short_name, score, result, match.id
        ))

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


@app.route("/user/<int:user_id>")
@login_required
@action_route
def user(user_id: int):
    """
    Shows a page describing a user/
    :param user_id: The ID of the user to display
    :return: The request response
    """
    user_data = User.query.get(user_id)
    if user_data is None:
        abort(404)

    bets = Bet.query.all()
    total_bets = len(list(filter(lambda x: x.user_id == user_id, bets)))
    bets = list(filter(lambda x: x.match.finished, bets))
    rr_bets = list(filter(lambda x: x.match.matchday > 17, bets))

    current_matchday, leaderboard_history = \
        generate_leaderboard_data(bets=bets)
    _, rr_history = generate_leaderboard_data(bets=rr_bets)

    bets = list(filter(lambda x: x.user_id == user_id, bets))

    total_points = 0
    for bet in bets:
        total_points += bet.evaluate(True)

    team_points = get_team_points_data(bets)[user_data]
    team_points = generate_team_points_table(team_points)

    points_distribution = generate_points_distributions(bets)[user_data]
    average_points = create_point_average_ranking(bets)[0][1]
    participation = create_participation_ranking(bets)[0][1]

    placements = leaderboard_history[user_data.username][1]
    rr_placements = rr_history[user_data.username][1]
    current_placement = "N/A"
    if len(placements) >= 1:
        current_placement = placements[len(placements) - 1]
    hinrunde_placement = "N/A"
    if len(placements) >= 17:
        hinrunde_placement = placements[16]
    ruckrunde_placement = "N/A"
    if len(rr_placements) >= 1:
        ruckrunde_placement = rr_placements[len(rr_placements) - 1]

    return render_template(
        "info/user.html",
        charts=True,
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
        player_best_team=team_points[0][0].name,
        player_worst_team=team_points[len(team_points) - 1][0].name,
        player_current_placement=current_placement,
        player_hinrunde_placement=hinrunde_placement,
        player_ruckrunde_placement=ruckrunde_placement,
        player_best_placement=min(placements),
        player_worst_placement=max(placements)
    )


@app.route("/stats", methods=["GET"])
@login_required
@action_route
def stats():
    """
    Displays a statistics page.
    :return: The Response
    """
    bets = Bet.query.all()
    finished_bets = list(filter(lambda x: x.match.finished, bets))

    leaderboards = []
    for _filter, bets_data, count in [
        (lambda x: x.match.matchday <= 17, bets, False),
        (lambda x: x.match.matchday > 17, bets, False),
        (lambda x: x.evaluate() == 15, finished_bets, True),
        (lambda x: x.evaluate() == 0, finished_bets, True)
    ]:
        dataset = list(filter(_filter, bets_data))

        leaderboard_action = LeaderboardAction.from_site_request()
        leaderboard_action.matchday = 34
        leaderboard_action.bets = dataset
        leaderboard_action.count = count
        leaderboards.append(leaderboard_action.execute()["leaderboard"])

    team_points = get_total_points_per_team(finished_bets)
    team_points = generate_team_points_table(team_points)

    points_distribution = {}
    for _, distrib in generate_points_distributions(finished_bets).items():
        for key, value in distrib.items():
            if key not in points_distribution:
                points_distribution[key] = 0
            points_distribution[key] += value

    participation_ranking = create_participation_ranking(finished_bets)
    average_ranking = create_point_average_ranking(finished_bets)

    return render_template(
        "info/stats.html",
        first_leaderboard=enumerate(leaderboards[0]),
        second_leaderboard=enumerate(leaderboards[1]),
        max_leaderboard=enumerate(leaderboards[2]),
        zero_leaderboard=enumerate(leaderboards[3]),
        team_points=enumerate(team_points),
        points_distribution=points_distribution,
        participation_ranking=enumerate(participation_ranking),
        average_ranking=enumerate(average_ranking),
        show_all=True,
        charts=True
    )
