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

from typing import Dict, Tuple, Callable
from bundesliga_tippspiel.background.season_events import handle_season_events
from bundesliga_tippspiel.background.reminders import send_due_reminders
from bundesliga_tippspiel.background.pointscalc import update_leaderboard
from bundesliga_tippspiel.background.openligadb import update_openligadb


bg_tasks: Dict[str, Tuple[int, Callable]] = {
    "update_db_data": (30, update_openligadb),
    "send_due_reminders": (60, send_due_reminders),
    "handle_season_events": (60 * 60 * 24, handle_season_events),
    "update_leaderboard": (30, update_leaderboard)
}
"""
A dictionary containing background tasks for the flask application
"""
