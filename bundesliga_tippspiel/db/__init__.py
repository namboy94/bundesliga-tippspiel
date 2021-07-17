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
from bundesliga_tippspiel.db.SeasonEvent import SeasonEvent
from bundesliga_tippspiel.db.match_data.Player import Player
from bundesliga_tippspiel.db.match_data.Goal import Goal
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.db.match_data.Team import Team
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.user_generated.SeasonWinner import SeasonWinner
from bundesliga_tippspiel.db.user_generated.ChatMessage import ChatMessage
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings
from bundesliga_tippspiel.db.user_generated.MatchdayWinner import \
    MatchdayWinner
from bundesliga_tippspiel.db.user_generated.UserProfile import UserProfile
from bundesliga_tippspiel.db.settings.DisplayBotsSettings import \
    DisplayBotsSettings
from bundesliga_tippspiel.db.user_generated.LeaderboardEntry import \
    LeaderboardEntry

models: List[db.Model] = [
    Player,
    Goal,
    Match,
    Team,
    Bet,
    SeasonWinner,
    MatchdayWinner,
    SeasonEvent,
    ReminderSettings,
    DisplayBotsSettings,
    ChatMessage,
    LeaderboardEntry,
    UserProfile
]
"""
The database models of the application
"""
