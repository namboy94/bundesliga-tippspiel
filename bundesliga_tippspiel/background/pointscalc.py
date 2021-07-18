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
from jerrycan.base import db, app
from jerrycan.db.User import User
from typing import List, Dict, Tuple
from bundesliga_tippspiel.db import Bet, Match, LeaderboardEntry, \
    DisplayBotsSettings, MatchdayWinner
from bundesliga_tippspiel.utils.matchday import get_matchday_info


def update_leaderboard():
    """
    Updates the leaderboard entries
    :return: None
    """
    start = time.time()
    app.logger.info("Updating leaderboard entries")
    update_bet_points()
    users = User.query.filter_by(confirmed=True).all()
    seasons = create_categorized_matches()
    season_points = calculate_matchday_points(users, seasons)
    process_matchday_winners(season_points)

    for (league, season), user_points in season_points.items():

        previous_positions = {}
        previous_no_bot_positions = {}
        user_totals = {user: 0 for user in users}
        for matchday, matchday_points in user_points.items():
            for user, points in matchday_points.items():
                user_totals[user] += points

            process_league_table(
                league,
                season,
                matchday,
                user_totals,
                previous_positions,
                previous_no_bot_positions
            )

    app.logger.debug(f"Finished leaderboard update in "
                     f"{time.time()-start:.2f}s")


def update_bet_points():
    """
    Updates the bet points
    :return: None
    """
    bets = Bet.query.options(db.joinedload(Bet.match)).all()
    for bet in bets:
        bet.points = bet.evaluate()
    db.session.commit()


def create_categorized_matches() -> Dict[
    Tuple[str, int], Dict[int, List[Match]]
]:
    """
    Sorts matches into seasons and matchdars
    :return: The matches categorized like this:
                {(league, season): {matchday: [match, ...]}}
    """
    seasons: Dict[Tuple[str, int], Dict[int, List[Match]]] = {}
    for match in Match.query.options(
            db.joinedload(Match.bets).subqueryload(Bet.user)
    ).all():
        league_season = (match.league, match.season)
        matchday = match.matchday
        if league_season not in seasons:
            seasons[league_season] = {}
        if matchday not in seasons[league_season]:
            seasons[league_season][matchday] = []
        seasons[league_season][matchday].append(match)
    return seasons


def calculate_matchday_points(
        users: List[User],
        seasons: Dict[Tuple[str, int], Dict[int, List[Match]]]
) -> Dict[Tuple[str, int], Dict[int, Dict[User, int]]]:
    """
    Calculates every user's points per matchday for each season
    :param users: The users to include
    :param seasons: The seasons data
    :return: {(league, season): {matchday: {user: points}}}
    """
    season_points = {}
    for league_season, season_data in seasons.items():

        user_points = {
            matchday: {user: 0 for user in users}
            for matchday in season_data.keys()
        }

        for matchday, matches in sorted(
                season_data.items(), key=lambda x: x[0]
        ):
            for match in matches:
                for bet in match.bets:
                    if bet.points is not None:
                        user_points[matchday][bet.user] += bet.points

        season_points[league_season] = user_points
    return season_points


def process_matchday_winners(
        per_matchday_data: Dict[Tuple[str, int], Dict[int, Dict[User, int]]]
):
    """
    Processes the matchday winners
    :param per_matchday_data: The points of each user per matchday
    :return: None
    """
    for (league, season), matchday_info in per_matchday_data.items():
        current_matchday = get_matchday_info(league, season)[0]
        for matchday, user_points in matchday_info.items():
            if matchday > current_matchday:
                continue

            best_user_id, best_points = None, 0
            for user, points in user_points.items():

                if DisplayBotsSettings.bot_symbol() in user.username:
                    continue
                if points > best_points:
                    best_user_id, best_points = user.id, points
                elif points == best_points:
                    best_user_id = None

            matchday_winner = MatchdayWinner(
                league=league,
                season=season,
                matchday=matchday,
                user_id=best_user_id
            )
            db.session.merge(matchday_winner)
    db.session.commit()


def process_league_table(
        league: str,
        season: int,
        matchday: int,
        user_points: Dict[User, int],
        previous_positions: Dict[User, int],
        previous_no_bot_positions: Dict[User, int]
):
    """
    Processes the league table entries and updates their corresponding database
    entries.
    :param league: The league to process
    :param season: The season to process
    :param matchday: The matchday to process
    :param user_points: The points for every user to process:
    :param previous_positions: Dictionary that keeps track of the previous
                               positions of the users
    :param previous_no_bot_positions: Dictionary that keeps track of the
                                      previous positions of the users
                                      disregarding bots
    :return: None
    """
    bot_symbol = DisplayBotsSettings.bot_symbol()
    ranking = [(user, points) for user, points in user_points.items()]
    ranking.sort(key=lambda x: x[0].id)
    ranking.sort(key=lambda x: x[1], reverse=True)

    no_bot_ranking = [x for x in ranking if bot_symbol not in x[0].username]
    no_bot_positions = {}
    for i, (user, _) in enumerate(no_bot_ranking):
        position = i + 1
        no_bot_positions[user] = position

    for i, (user, points) in enumerate(ranking):
        position = i + 1
        no_bot_position = no_bot_positions.get(user, position)

        previous_position = previous_positions.get(user, position)
        previous_positions[user] = position
        no_bot_previous_position = previous_no_bot_positions.get(
            user, no_bot_position
        )
        previous_no_bot_positions[user] = no_bot_position

        entry = LeaderboardEntry(
            league=league,
            season=season,
            matchday=matchday,
            user_id=user.id,
            points=points,
            position=position,
            no_bot_position=no_bot_position,
            previous_position=previous_position,
            no_bot_previous_position=no_bot_previous_position
        )
        db.session.merge(entry)
    db.session.commit()
