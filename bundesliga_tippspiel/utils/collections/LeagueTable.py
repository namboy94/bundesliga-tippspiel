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
from typing import Optional, List, Tuple, Dict, Union

from jerrycan.base import db
from jerrycan.db.User import User

from bundesliga_tippspiel.db import Match, Bet, Team


class LeagueTable:
    """
    Class that create a league table
    """

    def __init__(
            self,
            league: str,
            season: int,
            matchday: int,
            user: Optional[User]
    ):
        """
        Initializes the lague table object
        :param league: The league
        :param season: The season
        :param matchday: The matchday
        :param user: Optionally, a user. This will replace the real
                     results with the bets of the player
        """
        self.league = league
        self.season = season
        self.matchday = matchday
        self.user = user

        self.teams = Team.get_teams_for_season(league, season)
        self.matches = Match.query.filter_by(
            league=league, season=season
        ).filter(Match.matchday <= matchday).options(
            db.joinedload(Match.home_team),
            db.joinedload(Match.away_team)
        ).all()
        self.bets = []
        if self.user is not None:
            self.bets = [
                x for x in Bet.query.filter_by(
                    user_id=self.user.id,
                    league=league,
                    season=season
                ).options(db.joinedload(Bet.match)).all()
                if x.match.matchday <= matchday
            ]

    def calculate_table(self) -> List[Tuple[
        int, Team, int, int, int, int, int, int, int, int
    ]]:
        """
        Calculates the table
        :return: A list of tuples with the following items:
                    - position
                    - team
                    - matches
                    - wins
                    - draws
                    - losses
                    - goals for
                    - goals against
                    - goal difference
                    - points
        """
        teams = {team.abbreviation: team for team in self.teams}
        team_data = {
            team.abbreviation: {
                "matches": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "points": 0
            }
            for team in self.teams
        }
        handled = []
        match_infos = []
        for bet in self.bets:
            match = bet.match
            home = match.home_team_abbreviation
            away = match.away_team_abbreviation
            identifier = home + away + str(match.matchday)
            handled.append(identifier)

            if match.finished:
                match_infos.append(
                    (home, away, bet.home_score, bet.away_score)
                )

        for match in self.matches:
            home = match.home_team_abbreviation
            away = match.away_team_abbreviation
            identifier = home + away + str(match.matchday)
            if identifier in handled:
                continue

            if match.finished:
                match_infos.append(
                    (home, away, match.home_ft_score, match.away_ft_score)
                )

        for home, away, home_score, away_score in match_infos:
            for team, team_score, opponent_score in [
                (home, home_score, away_score),
                (away, away_score, home_score)
            ]:
                team_data[team]["matches"] += 1
                team_data[team]["goals_for"] += team_score
                team_data[team]["goals_against"] += opponent_score
                if team_score < opponent_score:
                    team_data[team]["losses"] += 1
                elif team_score > opponent_score:
                    team_data[team]["wins"] += 1
                    team_data[team]["points"] += 3
                else:
                    team_data[team]["draws"] += 1
                    team_data[team]["points"] += 1
        team_values = list(team_data.items())
        team_values.sort(key=lambda x: x[1]["points"], reverse=True)
        data_tuples = []
        for i, (team_abbreviation, data) in enumerate(team_values):
            data_tuples.append((
                i + 1,
                teams[team_abbreviation],
                data["matches"],
                data["wins"],
                data["draws"],
                data["losses"],
                data["goals_for"],
                data["goals_against"],
                data["goals_for"] - data["goals_against"],
                data["points"]
            ))
        return data_tuples
